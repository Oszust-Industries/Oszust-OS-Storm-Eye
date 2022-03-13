## Oszust OS Storm Eye - Setup Installer 1.0.0 - Oszust Industries
def clear(): return ("\n" * 70)
from os import path, walk
from win32com.client import Dispatch
import ctypes, os, shutil, sys, threading, urllib.request, win32com.client, zipfile

def setupConfig():
    global appBuild, appName, installLocation
    appName = "Oszust OS Storm Eye"
    installLocation = os.environ["ProgramFiles"] + "\\Oszust Industries\\" + appName
    appBuild = "Alpha"

def setupInstall():
    global errorCode, installStatus, installText
    errorCode, installStatus, installText, lastStatus = "", 0, "Starting Setup", 0
    if os.name != "nt":
        print("Update Failed (Not Windows)")
        exit()
    setupConfig()
    ##return ## STOPS THE INSTALLER
    OszustOSStormEyeSetupThread = threading.Thread(name="OszustOSStormEyeSetup", target=OszustOSStormEyeSetup)
    OszustOSStormEyeSetupThread.start()
    while installStatus < 10 and errorCode == "":
        if installStatus != lastStatus:
            print("\n" * 70)
            print(("\n" * 70) + installText + "... [" + ("=" * installStatus) + "]")
            lastStatus = installStatus
    if errorCode == "No_Internet":
        exitText = input(clear() + "The installer has failed. There doesn't seem to be any internet connection on your device. Press enter to quit installer...")
        exit()
    elif errorCode == "Packages_Failed":
        exitText = input(clear() + "The installer has failed. A required package failed to install. Press enter to quit installer...")
        exit()
    exitText = input(clear() + appName + " has finished installing. Press enter to quit installer...")
    os.remove(__file__)

def crashMessage():
    ## Display Crash
    global Argument
    import webbrowser
    webbrowser.open("https://github.com/Oszust-Industries/" + appName.replace(" ", "-"),  new = 2, autoraise = True)
    print(clear() + "Crash Log:\n" + ("-" * 50 + "\n") + str(Argument) + ("\n" + "-" * 50) + "\n")
    crash = input(appName + "'s installer has failed. Please report your crash to the issues tab in GitHub.\n\nPress enter to restart installer " + appName + "...\n")
    if crash not in ["exit()", "exit", "quit"]:
        try: setupInstall()
        except Exception as Argument: crashMessage()
    else: exit()

def OszustOSStormEyeSetup():
    global errorCode, installStatus, installText
    ## Threading - Auto Update App
    from urllib.request import urlopen
    installStatus, installText = 1, "Checking Internet"
    try: urlopen("http://google.com", timeout=1)
    except:
        errorCode = "No_Internet"
        return
    installStatus, installText = 2, "Creating Save Location"
    try:
        appNameDownload, appNameFile, appdata, objShell = appName.replace(" ", "_"), appName.replace(" ", "-"), os.getenv('APPDATA') + "\\Oszust Industries", win32com.client.Dispatch("WScript.Shell")
        if True:    
        ## Create Temp Folder for Update in Appdata
            if path.exists(appdata) == False: os.mkdir(appdata)
            if path.exists(appdata + "\\" + appName) == False: os.mkdir(appdata + "\\" + appName)
            if path.exists(appdata + "\\temp") == False: os.mkdir(appdata + "\\temp")
            else:
                shutil.rmtree(appdata + "\\temp")
                os.mkdir(appdata + "\\temp")
            os.umask(0)
            if not os.path.exists(os.environ["ProgramFiles"] + "\\Oszust Industries"): os.makedirs(os.environ["ProgramFiles"] + "\\Oszust Industries")
            if not os.path.exists(installLocation): os.makedirs(installLocation)
            else:
                shutil.rmtree(installLocation)
                os.makedirs(installLocation)
            installStatus, installText = 3, "Downloading"
            ## Download Update
            if appBuild.lower() == "main": urllib.request.urlretrieve("https://github.com/Oszust-Industries/"+appNameFile+"/archive/refs/heads/main.zip", str(os.getenv('APPDATA') + "\\Oszust Industries\\temp\\"+appNameDownload+".zip"))
            elif appBuild.lower() in ["alpha", "beta"]: urllib.request.urlretrieve("https://github.com/Oszust-Industries/"+appNameFile+"/archive/refs/heads/"+appBuild+".zip", str(os.getenv('APPDATA') + "\\Oszust Industries\\temp\\"+appNameDownload+".zip"))
            installStatus, installText = 5, "Extracting Files"
            with zipfile.ZipFile(appdata + "\\temp\\"+appNameDownload+".zip", 'r') as zip_ref: zip_ref.extractall(appdata + "\\temp")
            os.remove(appdata + "\\temp\\"+appNameDownload+".zip")
            if appBuild.lower() in ["alpha", "beta"]: os.rename(appdata + "\\temp\\"+appNameFile+"-"+appBuild, appdata + "\\temp\\"+appNameFile+"-Main")
            ## Update Required Files
            filenames = next(walk(appdata + "\\temp\\"+appNameFile+"-Main"), (None, None, []))[2]
            for i in filenames:
                try: os.remove(installLocation + "\\" + i)
                except: pass
                shutil.move(appdata + "\\temp\\"+appNameFile+"-Main\\" + i, installLocation)
            installStatus, installText = 7, "Creating Shortcut"
            ## Create Shortcut
            if path.exists(objShell.SpecialFolders("AllUsersPrograms") + "\\Oszust Industries") == False: os.mkdir(objShell.SpecialFolders("AllUsersPrograms") + "\\Oszust Industries")
            shell = Dispatch('WScript.Shell')
            try:
                shortcut = shell.CreateShortCut(objShell.SpecialFolders("AllUsersPrograms") + "\\Oszust Industries\\" + appName + ".lnk")
                shortcut.Targetpath = installLocation + "\\" + appName.replace(" ", "_") + ".py"
                shortcut.WorkingDirectory = installLocation
                shortcut.IconLocation = installLocation + "\\" + appName.replace(" ", "") + ".ico"
                shortcut.save()
            except: pass
            installStatus, installText = 8, "Installing Required Packages"
            ## Install Required Packages
            if installPackages() == "FAIL":
                errorCode = "Packages_Failed"
                return
            installStatus, installText = 9, "Finishing Setup"
            ## Clean Update
            shutil.rmtree(appdata + "\\temp")
            installStatus, installText = 10, "Done"
    except Exception as Argument: crashMessage()

def installPackages():
    try: from win10toast import ToastNotifier
    except:
        try:
            os.system("pip install win10toast")
            from win10toast import ToastNotifier
        except: return "FAIL"


## Start System
try:
    if ctypes.windll.shell32.IsUserAnAdmin(): setupInstall()
    else: ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
except Exception as Argument: crashMessage()
