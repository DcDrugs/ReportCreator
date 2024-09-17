import pyinstaller_versionfile
import PyInstaller.__main__
from settings import VERSION, PNAME

import sys
try:
    import os 
    os.system(".\qrc\docs\make.bat html")
except:
    pass

pyinstaller_versionfile.create_versionfile_from_input_file(
    output_file="metadata/versionfile.txt",
    input_file="metadata/metadata.yml",
    version=VERSION
)

PyInstaller.__main__.run([
    'main.py',
    '--noconfirm',
    '--noconsole',
    '--onefile',
    '--icon=qrc/icons/report.ico',
    '--add-data=./.venv/Lib/site-packages/pymorphy2_dicts_ru/data:pymorphy2_dicts_ru/data',
    '--version-file=metadata/versionfile.txt',
    '--name=' + PNAME
])