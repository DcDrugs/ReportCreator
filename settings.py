"""Файл с настройками
"""

import json
import sys
from wrapper import Wrapper
from logger import logging

from jsonpath_rw import parse

VERSION="3.2.0"
PNAME = "ReportCreator"

SETTINGS = 'settings'
jsonpath_expr = parse(SETTINGS + '..key.`parent`')

JSON_NAME = 'name'
JSON_VALUE = 'value'
JSON_TYPE = 'type'
JSON_KEY = 'key'

EXCEL = "Excel"
COMBOBOX = "Combobox" 
TEMPLATE = "Template" 
RESULT = "Result"
 

def read_config():
    """Чтение настроек

    Returns:
        json: настройки
    """
    file_contents = {}
    try:
        with open(SETTINGS + ".json", mode="r", encoding=sys.getdefaultencoding()) as user_file:
            file_contents = json.loads(user_file.read())
    except BaseException as ex:
        logging.error("BaseException",exc_info=True)
    return file_contents

# глобальные настройки
globalConfig = Wrapper({
    "settings": [
        {
            "key": "Settings",
            "name": "Общие настройки",
            "type": "group",
            "children": [
                {
                    "key": "Excel",
                    "name": "Excel файл",
                    "type": "file",
                    "value": None
                },
                {
                    "key": "Combobox",
                    "name": "Поиск осуществлять по",
                    "type": "str",
                    "value": None
                },
                {
                    "key": "Template",
                    "name": "Шаблон",
                    "type": "file",
                    "value": None
                },
                {
                    "key": "Result",
                    "name": "Результат",
                    "type": "file",
                    "value": None
                },
                {
                    "key": "DeleteTable",
                    "name": "Удаление первой таблицы",
                    "type": "bool",
                    "value": None
                }
            ]
        },
        {
            "key": "Battery",
            "name": "АКБ",
            "type": "group",
            "children": [
                {
                    "key": "Cost",
                    "name": "Цена за аккамулятор",
                    "type": "float",
                    "step": 0.01,
                    "decimals": 2,
                    "format": "{value}",
                    "value": None
                }
            ]
        },
        {
            "key": "Tire",
            "name": "Шины",
            "type": "group",
            "children": [
                {
                    "key": "TypeOfTire",
                    "name": "Тип шин",
                    "type": "list",
                    "value": None,
                    "limits": [
                        "Лето",
                        "Зима",
                        "Всесезонная"
                    ]
                },
                {
                    "key": "Cost_SH",
                    "name": "Цена за шину",
                    "type": "float",
                    "step": 0.01,
                    "decimals": 2,
                    "format": "{value}",
                    "value": None
                }
            ]
        }
    ]
})

def find(self, target: str):
    """поиск настроек

    Args:
        target (str): поиск настройки по ключу

    Returns:
        optional: настройка со всеми ключами
    """
    for item in self.items():
        if item.value[JSON_KEY] == target:
            return item.value
    return 

Wrapper.items = lambda self: jsonpath_expr.find(self.value)
Wrapper.find = lambda self, target: find(self, target)

def save_config():
    """сохранение настроек
    """
    with open(SETTINGS + ".json", mode="w", encoding=sys.getdefaultencoding()) as user_file:
            user_file.write(json.dumps(globalConfig.value, ensure_ascii=False, indent=4))

globalConfig.bind_to(lambda x : save_config())


def set_settings():
    dum = read_config()
    d = globalConfig.value
    for k,v in dum.items():
        d[k] = v
    globalConfig.value = d 
