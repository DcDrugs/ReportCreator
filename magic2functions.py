"""файл с магией, так как в стандартных библиотеках нашлись ошибки
"""

import jinja2
from docxtpl import DocxTemplate
import regex as re
DocxTemplate.source = None

r_xml_get_u_t = DocxTemplate.get_undeclared_template_variables
def get_undeclared_template_variables(self, jinja_env = None):
        """В этой функции исправили ошибку рендеринга без патча
        """
        self.init_docx(reload=False)
        xml = self.get_xml()
        xml = self.patch_xml(xml)
        for uri in [self.HEADER_URI, self.FOOTER_URI]:
            for relKey, part in self.get_headers_footers(uri):
                _xml = self.get_part_xml(part)
                xml += self.patch_xml(_xml)
        if jinja_env:
            env = jinja_env
        else:
            env = jinja2.Environment()
        xml = re.sub(
            r"<w:t(| .*?(?=>))>(.*?(?=</))</", 
            r"<w:t\1>\n\2\n</", xml, flags=re.U
        )
        parse_content = env.parse(xml)
        return jinja2.meta.find_undeclared_variables(parse_content)
DocxTemplate.get_undeclared_template_variables = get_undeclared_template_variables

r_xml_p = DocxTemplate.render_xml_part
def render_xml_part(self, src_xml, part, context, jinja_env=None):
    """В этой функции исправили ошибку не рабочего отладчика jinja2
    """
    src_xml = re.sub(
            r"<w:t(| .*?(?=>))>(.*?(?=</))</", 
            r"<w:t\1>\n\2\n</", src_xml, flags=re.U
        )
    src_xml = re.sub(r'<w:p([ >])', r'\n<w:p\1', src_xml)
    try:
        self.current_rendering_part = part
        if jinja_env:
            template = jinja_env.from_string(src_xml)
        else:
            template = jinja2.Template(src_xml)
        self.source = src_xml
        dst_xml = template.render(context)
    except jinja2.TemplateError as exc:
        if hasattr(exc, 'lineno') and exc.lineno is not None:
            line_number = max(exc.lineno - 4, 0)
            exc.docx_context = map(lambda x: re.sub(r'<[^>]+>', '', x),
                                    src_xml.splitlines()[line_number:(line_number + 7)])
        raise exc
    dst_xml = re.sub(r'\n<w:p([ >])', r'<w:p\1', dst_xml)
    dst_xml = re.sub(
            r"<w:t(| .*?(?=>))>\n(.*?(?=\n</))\n</", 
            r"<w:t\1>\2</", dst_xml
        )
    dst_xml = (dst_xml
                .replace('{_{', '{{')
                .replace('}_}', '}}')
                .replace('{_%', '{%')
                .replace('%_}', '%}'))
    dst_xml = self.resolve_listing(dst_xml)
    return dst_xml

DocxTemplate.render_xml_part = render_xml_part

s = jinja2.TemplateSyntaxError.__str__

def __str__(self) -> str:
    """В этой функции исправили ошибку не рабочего отладчика jinja2
    """
    self.translated = False
    return s(self)

jinja2.TemplateSyntaxError.__str__ = __str__

import re
import sys
tb_frame_re = re.compile(r"<frame at 0x[a-z0-9]*, file '(.*)', line (\d+), (?:code top-level template code|code template)>")
def jinja2_render_traceback(source):
    """В этой функции исправили ошибку не рабочего отладчика jinja2
    """
    traceback_print = ""
    # Get traceback objects
    typ, value, tb = sys.exc_info()
    # Iterate over nested traceback frames
    while tb:
        # Parse traceback frame string
        tb_frame_str = str(tb.tb_frame)
        tb_frame_match = tb_frame_re.match(tb_frame_str)
        tb_frame_istemplate = False
        # Identify frames corresponding to Jinja2 templates
        if tb.tb_frame.f_code.co_filename == '<template>':
            # Top-most template
            tb_src_path = '<unknown>'
            tb_lineno = tb.tb_lineno
            tb_frame_istemplate = True
        elif tb_frame_match:
            # nested child templates
            tb_src_path = tb_frame_match.group(1)
            tb_lineno = tb_frame_match.group(2)
            tb_frame_istemplate = True
            # Factorized string formatting
        if tb_frame_istemplate:
            location = f"line {tb_lineno}"
            name = tb_src_path
            if name:
                location = f'File "{name}", {location}'
            lines = [str(value), "  " + location]

            # if the source is set, add the line to the output
            if source is not None:
                try:
                    line = source.splitlines()[tb_lineno - 1]
                except IndexError:
                    pass
                else:
                    lines.append("    " + line.strip())


            value.args = ("\n".join(lines),)
            return value
        tb = tb.tb_next
    # Strip the final line jump
    return value
