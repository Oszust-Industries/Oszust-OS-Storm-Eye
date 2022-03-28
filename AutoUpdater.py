## Oszust OS Storm Eye - AutoUpdater 2.1.0 - Oszust Industries
from os import path, walk
from pathlib import Path
import os, shutil, threading, urllib.request, zipfile

def setupUpdate(systemName, systemBuild, systemVersion):
    global appName, appBuild, appVersion, UpdateStatus
    appName, appBuild, appVersion, UpdateStatus = systemName, systemBuild, systemVersion, -1
    ##return ## STOPS THE UPDATER
    if os.name != "nt": return "Update Failed (Not Windows)"
    ## Setup Thread and Return to Main App
    OszustOSStormEyeAutoUpdaterThread = threading.Thread(name="OszustOSStormEyeAutoUpdater", target=OszustOSStormEyeAutoUpdater)
    OszustOSStormEyeAutoUpdaterThread.start()
    return "Running Updater"

def OszustOSStormEyeAutoUpdater():
    global UpdateStatus
    ## Threading - Auto Update App
    ## Update statuses: -3 - No AppBuild, -2 - No Internet, 0 - None, 1 - Normal Update, 2 - Hotfix, 3 - LOCK
    from urllib.request import urlopen
    try: urlopen("http://google.com", timeout=1)
    except:
        UpdateStatus = -2
        return "No Internet"
    try:
        appNameDownload, appNameFile, appdata, current = appName.replace(" ", "_"), appName.replace(" ", "-"), os.getenv('APPDATA') + "\\Oszust Industries", str(Path(__file__).resolve().parent)
        if appBuild.lower() == "main":
            for line in urllib.request.urlopen("https://raw.githubusercontent.com/Oszust-Industries/"+appNameFile+"/Beta/Version.txt"):
                newestVersion = "".join([s for s in line.decode("utf-8") if s.strip("\r\n")])
        elif appBuild.lower() in ["alpha", "beta"]:
            for line in urllib.request.urlopen("https://raw.githubusercontent.com/Oszust-Industries/"+appNameFile+"/"+appBuild+"/Version.txt"):
                newestVersion = "".join([s for s in line.decode("utf-8") if s.strip("\r\n")])
        if newestVersion != appVersion:
            if "hotfix" in newestVersion.lower(): UpdateStatus = 2
            elif "emergency" in newestVersion.lower(): UpdateStatus = 3
            ## Create Temp Folder for Update in Appdata
            if path.exists(appdata) == False: os.mkdir(appdata)
            if path.exists(appdata+"\\temp") == False: os.mkdir(appdata + "\\temp")
            else:
                shutil.rmtree(appdata+"\\temp")
                os.mkdir(appdata+"\\temp")
            ## Download Update
            if appBuild.lower() in ["alpha", "beta", "main"]: urllib.request.urlretrieve("https://github.com/Oszust-Industries/"+appNameFile+"/archive/refs/heads/"+appBuild+".zip", str(os.getenv('APPDATA') + "\\Oszust Industries\\temp\\"+appNameDownload+".zip"))
            else:
                UpdateStatus = -3
                return "No AppBuild"
            with zipfile.ZipFile(appdata+"\\temp\\"+appNameDownload+".zip", 'r') as zip_ref: zip_ref.extractall(appdata+"\\temp")
            os.remove(appdata + "\\temp\\"+appNameDownload+".zip")
            if appBuild.lower() in ["alpha", "beta"]: os.rename(appdata +"\\temp\\"+appNameFile+"-"+appBuild, appdata +"\\temp\\"+appNameFile+"-Main")
            ## Update Required Files
            filenames = next(walk(appdata+"\\temp\\"+appNameFile+"-Main\\"), (None, None, []))[2]
            for i in filenames:
                try: os.remove(current+"\\"+i)
                except: pass
                shutil.move(appdata+"\\temp\\"+appNameFile+"-Main\\" + i, current)
            ## Required Packages
            packageManagement()
            ## Clean Update
            shutil.rmtree(appdata+"\\temp")
            if UpdateStatus == -1: UpdateStatus = 1
        else: UpdateStatus = 0
    except Exception as Argument: print("Update Failed (" + str(Argument) + ")")

def packageManagement():
    ## Insall/Update Required Packages
    try: from win10toast_click import ToastNotifier
    except:
        try:
            os.system("pip install win10toast-click -q")
            from win10toast_click import ToastNotifier
        except: return "FAIL"
