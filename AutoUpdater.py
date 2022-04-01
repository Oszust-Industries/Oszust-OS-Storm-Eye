## Oszust OS Storm Eye - AutoUpdater 2.3.0 - Oszust Industries
import os, pathlib, shutil, threading, urllib.request, urllib.request, zipfile

def setupUpdate(systemName, systemBuild, systemVersion):
    global UpdateStatus, appBuild, appName, appVersion, availableBuilds
    UpdateStatus, appBuild, appName, appVersion, availableBuilds = -1, systemBuild, systemName, systemVersion, ["Alpha"]
    ##return ## STOPS THE UPDATER
    if os.name != "nt": return "Update Failed (Not Windows)"
    ## Setup Thread and Return to Main App
    OszustOSAutoUpdaterThread = threading.Thread(name="OszustOSAutoUpdater", target=OszustOSAutoUpdater)
    OszustOSAutoUpdaterThread.start()
    return "Running Updater"

def OszustOSAutoUpdater():
    global UpdateStatus
    ## Threading - Auto Update App
    ## Update statuses: -3 - No AppBuild, -2 - No Internet, 0 - None, 1 - Normal Update, 2 - Hotfix, 3 - LOCK
    try: urllib.request.urlopen("http://google.com", timeout=3)
    except:
        UpdateStatus = -2
        return "No Internet"
    try:
        appNameDownload, appNameFile, docFolder, current = appName.replace(" ", "_"), appName.replace(" ", "-"), os.getenv('APPDATA') + "\\Oszust Industries", str(pathlib.Path(__file__).resolve().parent)
        if appBuild.lower() in availableBuilds:
            for line in urllib.request.urlopen("https://raw.githubusercontent.com/Oszust-Industries/"+appNameFile+"/"+appBuild+"/Version.txt"):
                newestVersion = "".join([s for s in line.decode("utf-8") if s.strip("\r\n")])
        else:
             UpdateStatus = -3
             return "No AppBuild"
        if newestVersion != appVersion:
            if "hotfix" in newestVersion.lower(): UpdateStatus = 2
            elif "emergency" in newestVersion.lower(): UpdateStatus = 3
        ## Create Temp Folder for Update in Appdata
            if os.path.exists(docFolder) == False: os.mkdir(docFolder)
            if os.path.exists(docFolder + "\\temp") == False: os.mkdir(docFolder + "\\temp")
            else:
                shutil.rmtree(docFolder + "\\temp")
                os.mkdir(docFolder + "\\temp")
        ## Download Update
            if appBuild.lower() in availableBuilds: urllib.request.urlretrieve("https://github.com/Oszust-Industries/"+appNameFile+"/archive/refs/heads/"+appBuild+".zip", str(os.getenv('APPDATA') + "\\Oszust Industries\\temp\\"+appNameDownload+".zip"))
            with zipfile.ZipFile(docFolder + "\\temp\\"+appNameDownload+".zip", 'r') as zip_ref: zip_ref.extractall(docFolder + "\\temp")
            os.remove(docFolder + "\\temp\\" + appNameDownload + ".zip")
            if appBuild.lower() != "main": os.rename(docFolder + "\\temp\\"+appNameFile+"-"+appBuild, docFolder + "\\temp\\"+appNameFile+"-Main")
        ## Update Required Files
            filenames = next(os.walk(docFolder + "\\temp\\" + appNameFile + "-Main\\"), (None, None, []))[2]
            for i in filenames:
                try: os.remove(current + "\\" + i)
                except: pass
                shutil.move(docFolder + "\\temp\\" + appNameFile + "-Main\\" + i, current)
        ## Install/Update Required Packages
            os.system('pip install pywin32 -q')
            os.system('pip install win10toast-click -q')
            os.system('pip install pysimplegui -q')
        ## Clean Update
            shutil.rmtree(docFolder + "\\temp")
            if UpdateStatus == -1: UpdateStatus = 1
        else: UpdateStatus = 0
    except Exception as Argument: print("Update Failed (" + str(Argument) + ")")
