from PyQt5 import QtWidgets
from pyqtgraph.parametertree import Parameter

from settings import SETTINGS, JSON_VALUE, globalConfig, save_config
        

def get_app():
    """получение API приложения

    Returns:
        QApplication: объект класса
    """
    app = QtWidgets.QApplication.instance()
    if app is None:
        # if it does not exist then a QApplication is created
        app = QtWidgets.QApplication([])
    return app

def create_params():
    """функция для создания параметров (Parameter Trees — pyqtgraph 0.14.0dev0)

        'bool':
        'value'
        'float':
        'value'
        'min'
        'max'
        'step'
        'dec'
        'siPrefix'
        'suffix'
        'decimals'
        'int'
        'str'
        =========================================================
        |limits     | [start, stop] numbers                     |
        =========================================================
        |step       | Defaults to 1, the spacing between each   |
        |           | slider tick                               |
        =========================================================
        |span       | Instead of limits + step, span can be set |
        |           | to specify the range of slider options    |
        |           | (e.g. np.linspace(-pi, pi, 100))          |
        =========================================================
        |format     | Format string to determine number of      |
        |           | decimals to show, etc. Defaults to display|
        |           | based on span dtype                       |
        =========================================================
        |precision  | int number of decimals to keep for float  |
        |           | tick spaces                               |
        =========================================================

    'group' Group parameters are used mainly as a generic parent item that holds (and groups!) a set of child parameters.

    It also provides a simple mechanism for displaying a button or combo that can be used to add new parameters to the group. To enable this, the group must be initialized with the ‘addText’ option (the text will be displayed on a button which, when clicked, will cause addNew() to be called). If the ‘addList’ option is specified as well, then a dropdown-list of addable items will be displayed instead of a button.

    'action': Used for displaying a button within the tree.


    'calendar': Displays a Qt calendar whose date is specified by a ‘format’ option.
        =========================================================
        |format     | Format for displaying the date and        |
        |           | converting from a string. Can be any      |
        |           | value accepted by QDate.toString and      |
        |           | fromString, or a stringified version of a |
        |           | QDateFormat enum, i.e. ‘ISODate’,         | 
        |           | ‘TextDate’ (default), etc.                | 
        =========================================================

    'checklist' Can be set just like a ListParameter, but allows for multiple values to be selected simultaneously.
        =========================================================
        |exclusive  | When False, any number of options can be  | 
        |           | selected. The resulting value() is a      |
        |           | list of all checked values. When True,    |
        |           | it behaves like a list type – only        |
        |           | one value can be selected. If no values   |
        |           | are selected and exclusive is set to      |
        |           | True, the first available limit is        |
        |           | selected. The return value of an          |
        |           | exclusive checklist is a single value     |
        |           | rather than a list with one element.      |
        =========================================================
        | delay     | Controls the wait time between editing    |
        |           | the checkboxes/radio button children and  |
        |           | firing a “value changed” signal. This     |
        |           | allows users to edit multiple boxes at    |
        |           | once for a single value update.           |
        =========================================================

    'color'

    'colormap'

    'file' Interfaces with the myriad of file options available from a QFileDialog. Note that the output can either be a single file string or list of files, depending on whether fileMode=’ExistingFiles’ is specified. Note that in all cases, absolute file paths are returned unless relativeTo is specified as elaborated below.
        =========================================================
        |parent     | Dialog parent                             |
        =========================================================
        |winTitle   | Title of dialog window                    |
        =========================================================
        |nameFilter | File filter as required by the Qt dialog  |
        =========================================================
        |directory  | Where in the file system to open this     |
        |           | dialog                                    |
        =========================================================
        |selectFile | File to preselect                         |
        =========================================================
        |relativeTo | Parent directory that, if provided, will  | 
        |           | be removed from the prefix of all returned| 
        |           | paths. So, if ‘/my/text/file.txt’ was     |
        |           | selected, and relativeTo=’my/text/’, the  |
        |           | return value would be ‘file.txt’. This    |
        |           | uses os.path.relpath under the hood, so   |
        |           | expect that behavior.                     |
        =========================================================
        |kwargs     | Any enum value accepted by a QFileDialog  |
        |           | and its value. Values can be a string or  |
        |           | list of strings, i.e. fileMode=’AnyFile’, |
        |           | options=[‘ShowDirsOnly’,                  |
        |           |‘DontResolveSymlinks’]                     |
        =========================================================

    'font' Creates and controls a QFont value. Be careful when selecting options from the font dropdown. since not all fonts are available on all systems

    'list' Parameter with a list of acceptable values. By default, this parameter is represtented by a ListParameterItem, displaying a combo box to select a value from the list. In addition to the generic Parameter options, this parameter type accepts a limits argument specifying the list of allowed values. The values may generally be of any data type, as long as they can be represented as a string. If the string representation provided is undesirable, the values may be given as a dictionary mapping the desired string representation to the value.

    'pen' Controls the appearance of a QPen value. When saveState is called, the value is encoded as (color, width, style, capStyle, joinStyle, cosmetic)
        =========================================================
        |color      | pen color, can be any argument accepted by| 
        |           | mkColor() (defaults to black)             |
        =========================================================
        |width      | integer width >= 0 (defaults to 1)        |
        =========================================================
        |style      | String version of QPenStyle enum, i.e.    | 
        |           | ‘SolidLine’ (default), ‘DashLine’, etc.   |
        =========================================================
        |capStyle   | String version of QPenCapStyle enum, i.e. |
        |           | ‘SquareCap’ (default), ‘RoundCap’, etc.   |
        =========================================================
        |joinStyle  | String version of QPenJoinStyle enum, i.e.| 
        |           | ‘BevelJoin’ (default), ‘RoundJoin’, etc.  |
        =========================================================
        |cosmetic   | Boolean, whether or not the pen is        |
        |           | cosmetic (defaults to True)               |
        =========================================================

    'progress' Displays a progress bar whose value can be set between 0 and 100

    'slider'

    'text' Editable string, displayed as large text box in the tree.

    Returns:
        Parameter: дерево настроек
    """
    params = Parameter.create(name='Parameters', type='group', children=globalConfig.value[SETTINGS])
    
    def a(param, value):
        """обработчик сигналов изменений значений настроек для их дальнейшего сохранения

        Args:
            param (dict): информация о настройке
            value (optional): новое значение
        """
        globalConfig.find(param.opts['key'])[JSON_VALUE] = value
        save_config()

        
    def onChange(_param, _value):
        """Обработчик

        Args:
            param (dict): информация о настройке
            value (optional): новое значение
        """
        a(_param, _value)

    def connect_r(obj):
        """функция для подключения дерева настроек к обработчику

        Args:
            obj (Parameter): параметр
        """
        if obj.type() == "group":
            for o in obj.children():
                connect_r(o)
        obj.sigValueChanged.connect(onChange)
    connect_r(params)    
    return params