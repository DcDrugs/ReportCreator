"""файл для увеличения функционала jinja2

доступные функции в jinja2:

jin.globals.update(deviation=deviation)

jin.globals.update(handle_catch=handle_catch)

jin.globals.update(numpy=numpy)

jin.globals.update(relativedelta=relativedelta)

jin.globals.update(jin=jin)

jin.globals.update(docxtpl=docxtpl)

jin.globals.update(jdebug=jdebug)

jin.globals['import'] = import_custom_lib

jin.globals['raise'] = raise_helper

jin.filters["format"] = morph_format

from doctemp
jin.globals.update(get=get)

jin.globals.update(find=find)

"""

import jinja2
import sys
import os
import pathlib
import importlib
from pathlib import Path
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.environ["PYMORPHY2_DICT_PATH"] = str(pathlib.Path(sys._MEIPASS).joinpath('pymorphy2_dicts_ru/data'))
import math
import pymorphy2
from pyphrasy.inflect import PhraseInflector
import datetime
import docxtpl
import logging
import numpy
import builtins
from memoization import cached
from dateutil import relativedelta
import calendar
from jinja2.filters import do_format

from morthNumber import MorphNumber
from PyQt5.QtWidgets import QMessageBox


morph = pymorphy2.MorphAnalyzer()
inflector = PhraseInflector(morph)
MORPH = MorphNumber()
error_text = "#ЗНАЧ"
error = docxtpl.RichText(error_text)

def wrapper_error(func):
    """Враппер для отова ошибок

    Args:
        func (_type_): функция, которая может выкинуть ошибку
    """
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BaseException as err:
            logging.error("BaseException",exc_info=True)
            return error_text

    return wrap

@wrapper_error
def deviation(phrase: str, grammers: list):
    """Эта функция необходима для склонения фраз благодаря pymorphy2
        Часть речи
    Граммема	Значение	Примеры
    NOUN	имя существительное	хомяк
    ADJF	имя прилагательное (полное)	хороший
    ADJS	имя прилагательное (краткое)	хорош
    COMP	компаратив	лучше, получше, выше
    VERB	глагол (личная форма)	говорю, говорит, говорил
    INFN	глагол (инфинитив)	говорить, сказать
    PRTF	причастие (полное)	прочитавший, прочитанная
    PRTS	причастие (краткое)	прочитана
    GRND	деепричастие	прочитав, рассказывая
    NUMR	числительное	три, пятьдесят
    ADVB	наречие	круто
    NPRO	местоимение-существительное	он
    PRED	предикатив	некогда
    PREP	предлог	в
    CONJ	союз	и
    PRCL	частица	бы, же, лишь
    INTJ	междометие	ой
        Падеж
    Граммема	Значение	Пояснение	Примеры
    nomn	именительный	Кто? Что?	хомяк ест
    gent	родительный	Кого? Чего?	у нас нет хомяка
    datv	дательный	Кому? Чему?	сказать хомяку спасибо
    accs	винительный	Кого? Что?	хомяк читает книгу
    ablt	творительный	Кем? Чем?	зерно съедено хомяком
    loct	предложный	О ком? О чём? и т.п.	хомяка несут в корзинке
    voct	звательный	Его формы используются при обращении к человеку.	Саш, пойдем в кино.
    gen2	второй родительный (частичный)	 	ложка сахару (gent - производство сахара); стакан яду (gent - нет яда)
    acc2	второй винительный	 	записался в солдаты
    loc2	второй предложный (местный)	 	я у него в долгу (loct - напоминать о долге); висит в шкафу (loct - монолог о шкафе); весь в снегу (loct - писать о снеге)
        Число
    Граммема	Значение	Примеры
    sing	единственное число	хомяк, говорит
    plur	множественное число	хомяки, говорят
        Род
    Граммема	Значение	Примеры
    masc	мужской род	хомяк, говорил
    femn	женский род	хомячиха, говорила
    neut	средний род	зерно, говорило
    Args:
        phrase (str): фраза для преобразования в нужную часть речи/число/падеж
        grammers (list): список грамматики, который должен быть характерен для данной фразы
    Returns:
        str: преобразованный текст
    """
    return inflector.inflect(phrase, grammers)

@wrapper_error 
def handle_catch(caller, on_exception):
    """Отлавливаем ошибки в jinja2

    Args:
        caller (_type_): фунция, которая может выкинуть ошибку
        on_exception (_type_): сообщение при ошибке вместо результата функции

    Returns:
        _type_: _description_
    """
    try:
         return caller()
    except BaseException as ex:
        print(ex)
        return on_exception
    
def raise_helper(msg):
    """Получить ошибку из шаблона jinja2

    Args:
        msg (_type_): сообщение

    Raises:
        Exception: ошибка
    """
    raise Exception(msg)

# use an existing filter so as not to get an initialization error
@wrapper_error
def morph_format(value: int, *args, **kwargs):
    """Эта функция необходима для согласования фразы с числительными
    Args:
        value (int): число с которым нужно согласовать фразу
        *args: используеться в случае, если не указан morph в kwargs в do_format
        **kwargs: используеться в случае, если не указан morph в kwargs в do_format
            ключи для дополнительного функционала
                "morph" - фраза, которую необходимо согласовать с числительным
                    str: В morph желательно писать слово/фразу, согласованную с цифрой 1
                    list[str]: Ручной шаблон согласования. В случае, если автоматическая морфология допускает ошибки. Укажите слова для чисел: 1, 2, 5.
                "as_ordinal" - Порядковые числительные
                    В morph нужно указать пример, в какую форму преобразовать числительное.
                    и снова {{ 3|format(morph='первое', as_ordinal=True) }} сентября => и снова третье сентября
                "reverse"  - Обратное преобразование
                    {{ "два миллиона четыреста тридцать пять"|format(morph='', reverse=true) }} => 2000435
                "as_text" 
                    Число без согласования
                    bool: true
                        {{ 2000435|format(morph='') }} => два миллиона четыреста тридцать пять
                    bool: false
                        {{ 2000435|format(morph='', as_text=false) }} => 2000435
                    Согласование без вывовда числа
                    None
                    {{ 5|format(morph='просроченная задача', as_text=None) }} => просроченных задач
        phrase (str): фраза для преобразования в нужную часть речи/число/падеж
        grammers (list): список грамматики, который должен быть характерен для данной фразы
    Returns:
        str: преобразованный текст
    """
    if "morph" in kwargs:
        if kwargs.get("as_ordinal"):
            return MORPH.number_to_ordinal(value, kwargs["morph"])

        if kwargs.get("reverse"):
            return MORPH.text_to_integer(value)

        as_text = kwargs.get("as_text", True)

        if isinstance(kwargs["morph"], list):
            return MORPH.number_with_custom_text(value, kwargs["morph"], as_text)

        return MORPH.number_with_text(value, kwargs["morph"], as_text)

    else:
        return do_format(value, *args, **kwargs)
    
def jdebug(*args, **kwargs):
    """Эта функция необходима для отлаживания информации подсчета в документе
        *args: данные для вывода в сообщение
        **kwargs: данные для вывода в сообщение
    """
    kwargsString = ", ".join(f"{str(key)}={str(value)}" for key, value in kwargs.items())
    QMessageBox.information(None, 'Debug', "debug command: args: \"%s\" kwargs: \"%s\"" % (', '.join(map(str, args)), kwargsString))
       
def import_custom_lib(module):
    """Эта функция необходима для подключения библиотек внутри документа
        module: имя модуля или его путь
    Returns:
        module - собранный и готовый к работе модуль
    """
    module1 = os.path.abspath(module)
    if os.path.isfile(module1):
        name =  Path(module1).stem
        spec = importlib.util.spec_from_file_location(name, os.path.abspath(module1))
        foo = importlib.util.module_from_spec(spec)
        sys.modules[name] = foo
        spec.loader.exec_module(foo)
        return foo
    else:
        try:
            return importlib.import_module(module)
        except TypeError as t:
            t.args = (*t.args, str(module1) + " is not found")
            raise
       
jin = jinja2.Environment()
jin.globals.update(deviation=deviation)
jin.globals.update(handle_catch=handle_catch)
jin.globals.update(numpy=numpy)
jin.globals.update(relativedelta=relativedelta)
jin.globals.update(jin=jin)
jin.globals.update(docxtpl=docxtpl)
jin.globals.update(jdebug=jdebug)
jin.globals['import'] = import_custom_lib
jin.globals['raise'] = raise_helper

jin.filters["format"] = morph_format