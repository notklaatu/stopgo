;2014-04-13, all-in-one installer for StopGo's dependencies (Windows).
Name "Python Bundle for StopGo"
OutFile "stopgo_dependencies.exe"
ShowInstDetails hide

!Include "ZipDLL.nsh"

InstallDir "C:\Python27\"

Section "Python 2.7.9"
	SetOutPath "C:\"
	File "python-2.7.9.msi"
	ExecWait '"msiexec.exe" /i C:\python-2.7.9.msi'
	Delete "C:\python-2.7.9.msi"
SectionEnd

Section "wxPython 3.0.2.0"
	MessageBox MB_OK "About to install wxPython."
	SetOutPath $INSTDIR
	File "wxPython3.0-win32-3.0.2.0-py27.exe"
	ExecWait "C:\Python27\wxPython3.0-win32-3.0.2.0-py27.exe"
	Delete "C:\Python27\wxPython3.0-win32-3.0.2.0-py27.exe"
SectionEnd

Section "Setuptools 20.1.1"
    SetOutPath $INSTDIR
    File ez_setup.py
	DetailPrint "Executing ez_setup.py for Python setuptools..."
	nsExec::ExecToLog '"C:\Python27\python.exe" ez_setup.py'
SectionEnd

Section "WinFF 1.5.4"
	SetOutPath "C:\"
	File "WinFF-1.5.4-Setup-3.exe"
	ExecWait "C:\WinFF-1.5.4-Setup-3.exe"
	Delete "C:\WinFF-1.5.4-Setup-3.exe"
	Push "PATH"
	Push $INSTDIR
	Call AddToEnvVar
	MessageBox MB_OK "Installation Complete"
SectionEnd
