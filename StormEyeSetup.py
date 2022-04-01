## Oszust OS Storm Eye - Setup Installer 2.0.0 - Oszust Industries
installerVersion = "v2.0.0"
import os, sys
def fixPython():
    print("Installing Python Packages...")
    try: os.system('pip install pywin32 -q')
    except:
        exitText = input("Error 01: The installer has failed. You seem to not have the correct Python installed. Press enter to quit installer...")
        exit()
    try: os.system('pip install pysimplegui -q')
    except:
        exitText = input("Error 02: The installer has failed. You seem to not have the correct Python installed. Press enter to quit installer...")
        exit()
    os.execv(sys.executable, ['python'] + sys.argv)
try:
    from win32com.shell import shell, shellcon
    import PySimpleGUI as sg
except: fixPython()
import ctypes, shutil, threading, urllib.request, urllib.request, win32com.client, zipfile

def setupConfig():
    global appBuild, appName, installLocation, availableBuilds
    appName, appBuild, availableBuilds = "Oszust OS Storm Eye", "Alpha", ["Alpha"]
    installLocation = os.environ["ProgramFiles"] + "\\Oszust Industries\\" + appName

def showErrorMessage(message):
    import webbrowser
    window = sg.Window("Installer - ERROR", [[sg.Text(message)], [sg.Button("Report Error", button_color=("White", "Blue"), key='Report'), sg.Button("Quit", button_color=("White", "Red"), key='Quit')]], size=(320, 100), resizable=False, finalize=True, element_justification='c')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Quit': exit()
        elif event == 'Report': webbrowser.open("https://github.com/Oszust-Industries/" + appName.replace(" ", "-") + "/issues/new",  new = 2, autoraise = True)

def setupInstall():
    global DesktopShortcut, appBuild, errorCode, installLocation, installStatus, installText
    DesktopShortcut, errorCode, installStatus, installText, lastStatus = True, "", 0, "Starting Setup", 0
    print("Starting Installer...\nLaunching Interface...")
    sg.theme('Dark2')
    setupConfig()
    if os.name not in ["nt"]: showErrorMessage("Error 03: This program is built only for Windows devices.")
    if sys.version_info >= (3, 7) == False: showErrorMessage("Error 04: You seem to have an old version of Python installed. The program requires v3.7.0 or higher.")
    ## Interface Creator
    layout = [[sg.vbottom([sg.Text(appName+" Installer",font=("Helvetica", 18)), sg.Text(installerVersion,font=("Helvetica", 12), justification='center', text_color = 'Light Blue')])],
              [sg.Text("Install program to:", font=("Helvetica", 12)), sg.InputText(installLocation, size=(60, 20), key='installLocation'), sg.FolderBrowse(target='installLocation')],
              [sg.Text("Build:", font=("Helvetica", 12)), sg.Combo(availableBuilds, default_value=appBuild, key='buildInput')],
              [sg.Text("Create Desktop shortcut", font=("Helvetica", 12)), sg.Checkbox("", default=True, key='startMenuCheckbox')],
              [sg.Button("Start Install", button_color=('White', 'Green'), key='startInstallButton')],
              [sg.Text(installText+"...", key='installText', font=("Ariel", 12), visible=False)],
              [sg.ProgressBar(50, orientation='h', size=(20, 10), border_width=4, key='progbar', bar_color=['Green','White'], visible=False)]]
    window = sg.Window(appName + " Installer", layout, resizable=True, finalize=True, element_justification='c')
    window.maximize()
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: exit()
        elif event == 'startInstallButton':
            installLocation = values['installLocation']
            appBuild = values['buildInput']
            DesktopShortcut = values['startMenuCheckbox']
            window['startInstallButton'].update(visible=False)
            window['installText'].update(visible=True)
            window['progbar'].update(visible=True)
            break
    ## Check Appbuild
    if appBuild not in availableBuilds:
        window['installText'].update("Error.")
        sg.Popup("A requested app build does not exist.", title="No App Build")
        window.close()
        setupInstall()
        return
    OszustOSSetupInstallerThread = threading.Thread(name='OszustOSSetupInstaller', target=OszustOSSetupInstaller)
    OszustOSSetupInstallerThread.start()
    while installStatus < 10 and errorCode == "":
        if installStatus != lastStatus:
            window['installText'].update(installText + "...")
            window['progbar'].UpdateBar(installStatus, 10)
            lastStatus = installStatus
    if errorCode == "No_Internet": showErrorMessage("Error 05: There doesn't seem to be any internet connection on your device.")
    elif errorCode == "Packages_Failed": showErrorMessage("Error 06: A required package failed to install.")
    window['installText'].update("Done.")
    window['progbar'].UpdateBar(10, 10)
    window = sg.Window("Installer - FINISH", [[sg.Text(appName + " has finished installing!")], [sg.Button("Done", button_color=('White', 'Green'), key='DoneButton')]], size=(320, 100), resizable=False, finalize=True, element_justification='c')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'DoneButton':
            os.remove(__file__)
            exit()

def OszustOSSetupInstaller():
    global errorCode, installStatus, installText
    ## Threading - Installer
    installStatus, installText = 1, "Checking Internet"
    try: urllib.request.urlopen("http://google.com", timeout=3)
    except:
        errorCode = "No_Internet"
        return
    installStatus, installText = 2, "Creating Save Location"
    if True:
        appNameDownload, appNameFile, docFolder, objShell = appName.replace(" ", "_"), appName.replace(" ", "-"), shell.SHGetFolderPath(0, shellcon.CSIDL_PERSONAL, None, 0) + "\\Oszust Industries", win32com.client.Dispatch("WScript.Shell")
    ## Create Temp Folder for Update in Documents
        if os.path.exists(docFolder) == False: os.mkdir(docFolder)
        if os.path.exists(docFolder + "\\" + appName) == False: os.mkdir(docFolder + "\\" + appName)
        if os.path.exists(docFolder + "\\temp") == False: os.mkdir(docFolder + "\\temp")
        else:
            shutil.rmtree(docFolder + "\\temp")
            os.mkdir(docFolder + "\\temp")
        if (os.environ["ProgramFiles"] + "\\Oszust Industries" in installLocation) and not os.path.exists(os.environ["ProgramFiles"] + "\\Oszust Industries"): os.mkdir(os.environ["ProgramFiles"] + "\\Oszust Industries")
        if not os.path.exists(installLocation): os.mkdir(installLocation)
        else:
            shutil.rmtree(installLocation)
            os.mkdir(installLocation)
        os.system('ICACLS "'+installLocation+'" /grant Users:(OI)(CI)F /T')
    ## Download Update
        installStatus, installText = 3, "Downloading"
        urllib.request.urlretrieve("https://github.com/Oszust-Industries/"+appNameFile+"/archive/refs/heads/"+appBuild+".zip", (docFolder+"\\temp\\"+appNameDownload+".zip"))
        installStatus, installText = 5, "Extracting Files"
        with zipfile.ZipFile(docFolder+"\\temp\\"+appNameDownload+".zip", 'r') as zip_ref: zip_ref.extractall(docFolder + "\\temp")
        os.remove(docFolder + "\\temp\\" + appNameDownload + ".zip")
        if appBuild.lower() != "main": os.rename(docFolder + "\\temp\\"+appNameFile+"-"+appBuild, docFolder + "\\temp\\"+appNameFile+"-Main")
    ## Move Required Files
        filenames = next(os.walk(docFolder + "\\temp\\" + appNameFile + "-Main"), (None, None, []))[2]
        for i in filenames:
            try: os.remove(installLocation + "\\" + i)
            except: pass
            shutil.move(docFolder + "\\temp\\" + appNameFile + "-Main\\" + i, installLocation)
    ## Create Shortcut
        installStatus, installText = 7, "Creating Shortcut"
        try: os.remove(objShell.SpecialFolders("AllUsersPrograms") + "\\Oszust Industries\\" + uninstallerPath.split("\\")[-1] + ".lnk") ## Delete Start Menu Shortcut
        except: pass
        try: os.remove(shell.SHGetFolderPath (0, shellcon.CSIDL_DESKTOP, 0, 0) + "\\" + uninstallerPath.split("\\")[-1] + ".lnk") ## Delete Desktop Shortcut
        except: pass
        if os.path.exists(objShell.SpecialFolders("AllUsersPrograms") + "\\Oszust Industries") == False: os.mkdir(objShell.SpecialFolders("AllUsersPrograms") + "\\Oszust Industries")
        try:
            for i in range(1,3):
                if i == 1: shortcut = win32com.client.Dispatch('WScript.Shell').CreateShortCut(objShell.SpecialFolders("AllUsersPrograms") + "\\Oszust Industries\\" + appName + ".lnk")
                elif i == 2 and DesktopShortcut == True: shortcut = win32com.client.Dispatch('WScript.Shell').CreateShortCut(shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, 0, 0) + "\\" + appName + ".lnk")
                shortcut.Targetpath = installLocation + "\\" + appName.replace(" ", "_") + ".py"
                shortcut.IconLocation = installLocation + "\\" + appName.replace(" ", "") + ".ico"
                shortcut.save()
        except: pass
    ## Install Required Packages
        installStatus, installText = 8, "Installing Required Packages"
        if installPackages() == "FAIL":
            errorCode = "Packages_Failed"
            return
    ## Clean Update
        installStatus, installText = 9, "Finishing Setup"
        shutil.rmtree(docFolder + "\\temp")
        installStatus, installText = 10, "Done"

def installPackages():
    try:
        os.system('pip install win10toast-click -q')
        from win10toast_click import ToastNotifier
    except: return "FAIL"
    try:
        os.system('pip install pysimplegui -q')
        import PySimpleGUI as sg
    except: return "FAIL"


## Start System
try:
    if ctypes.windll.shell32.IsUserAnAdmin(): setupInstall()
    else: ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
except Exception as Argument: showErrorMessage("Error 00: " + str(Argument))
