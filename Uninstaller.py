## Uninstaller 1.1.0 - Oszust Industries
from win32com.shell import shell, shellcon
import os, shutil, win32com.client
objShell, uninstallerPath = win32com.client.Dispatch("WScript.Shell"), os.path.dirname(os.path.realpath(__file__))
try: os.remove(objShell.SpecialFolders("AllUsersPrograms") + "\\Oszust Industries\\" + uninstallerPath.split("\\")[-1] + ".lnk") ## Delete Start Menu Shortcut
except: pass
try: os.remove(shell.SHGetFolderPath (0, shellcon.CSIDL_DESKTOP, 0, 0) + "\\" + uninstallerPath.split("\\")[-1] + ".lnk") ## Delete Desktop Shortcut
except: pass
shutil.rmtree(uninstallerPath) ## Delete Program
