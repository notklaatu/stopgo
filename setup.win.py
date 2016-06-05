import sys
from cx_Freeze import setup, Executable
import os

sys.path.append(os.path.join("usr","share","pyshared","stopgolibs"))
# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os","app"], "excludes": ["tkinter","tcl","tk"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "StopGo",
        version = "0.0.9",
        description = "StopGo Stop Motion Animation",
        options = {"build_exe": build_exe_options},
        include_files = (os.path.join("usr","share","pyshared","stopgolibs")),
        executables = [Executable(os.path.join("usr","bin","stopgo"), base=base)])
