import sys
from cx_Freeze import setup,Executable

import os

os.environ['TCL_LIBRARY'] = "C:\\LOCAL_TO_PYTHON\\Python35-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\LOCAL_TO_PYTHON\\Python35-32\\tcl\\tk8.6"

base = None
if sys.platform == 'win32' : 
    base = "Win32GUI"

setup( name="PY_AUTO_RAGNAROK",
        version="1.0",
        executables = [Executable("RAGNAROK_AUTO_PLAY.py",base=base)])