## Uninstaller 1.0.0 - Oszust Industries
from os import path
import os, shutil, win32com.client
##exit() ## STOPS THE UNINSTALLER
objShell, uninstallerPath = win32com.client.Dispatch("WScript.Shell"), os.path.dirname(os.path.realpath(__file__))
try: os.remove(objShell.SpecialFolders("AllUsersPrograms") + "\\Oszust Industries\\" + uninstallerPath.split("\\")[-1]) ## Delete Shortcut
except: pass
shutil.rmtree(uninstallerPath) ## Delete Program
