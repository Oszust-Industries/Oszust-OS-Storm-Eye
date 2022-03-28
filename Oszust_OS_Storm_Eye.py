## Oszust OS Storm Eye - Oszust Industries
## Created on: 12-16-21 - Last update: 3-28-21
softwareVersion = "ALPHA-v1.0.1.025"
def clear(): return ("\n" * 70)
from urllib.request import urlopen
from pathlib import Path
import threading, datetime, json, os, pickle
def openChangelog(): webbrowser.open_new("https://github.com/Oszust-Industries/" + systemName.replace(" ", "-") + "/releases")
import AutoUpdater

def softwareConfig():
    import uuid
    ## System Configuration
    global appBuild, appdata, deactivateFileOpening, exitSystem, resetSettings, systemName, MeasurementUnits, HourlyForecastScale, apiKey, recentSearches
    appdata, systemName, exitSystem = os.getenv('APPDATA') + "\\Oszust Industries\\", "Oszust OS Storm Eye", False
    try:
        configFile = json.load(open(appdata + systemName + "\\Config.json",))
        appBuild, apiKey, resetSettings, deactivateFileOpening, MeasurementUnits, HourlyForecastScale = configFile["appBuild"], configFile["userAPIKey"], configFile["resetSettings"], configFile["deactivateFileOpening"], configFile["MeasurementUnits"], configFile["HourlyForecastScale"]
    except:
        ## Create new .json file for configs
        if os.path.isfile(appdata + systemName + "\\Config.json") == False:
            with open(appdata + systemName + "\\Config.json", 'w') as f: json.dump({}, f, indent=4)
        with open(appdata + systemName + "\\Config.json", 'r') as f:
            data = json.load(f)
            data = {"appBuild": "Alpha","userAPIKey": "","resetSettings": False,"deactivateFileOpening": False,"MeasurementUnits": "Imperial","HourlyForecastScale": 12}
            tempfile = os.path.join(os.path.dirname(appdata + systemName + "\\Config.json"), str(uuid.uuid4()))
        with open(tempfile, 'w') as f: json.dump(data, f, indent=4)
        os.remove(appdata + systemName + "\\Config.json")
        os.rename(tempfile, appdata + systemName + "\\Config.json")
        softwareConfig()
    try:
        recentSearches = pickle.load(open(appdata + systemName + "\\Recent.p", "rb"))
    except:
        recentSearches = []
        pickle.dump(recentSearches, open(appdata + systemName + "\\Recent.p", "wb"))

def softwareSetup():
    ## Setup Software
    global accountReady, restartNeed, deactivateFileOpening
    print("Loading...")
    softwareConfig()
    serverActions("wifiTest")
    AutoUpdater.setupUpdate(systemName, appBuild, softwareVersion)
    serverActions("updateStatusCheckThreadStart")
    serverActions("startAchievementSystem")
    if apiKey == "":
        serverActions("apiSetup")
        return
    ## Start Functions
    if exitSystem == False:
        if os.name != "nt": deactivateFileOpening = True  ## Windows Detector
        print(clear())
        mainMenu()

def serverActions(Action):
    global exitSystem, toaster, userAPIKey
    if Action == "wifiTest":
        from urllib.request import urlopen
        try: urlopen("http://google.com", timeout=1)
        except: serverActions("noWifi")
    elif Action == "noWifi":
        import random
        print(clear() + "There doesn't seem to be any internet connection on your device.\n" + systemName + " needs internet to display the weather.\n")
        retry = input("\"" + random.choice(open("./Wifi text.txt").read().splitlines()) + "\"\n\nPress any key to retry the internet connection...")
        print(clear())
        softwareSetup()
    elif Action == "updateStatusCheckThreadStart":
        checkUpdateStatusThread = threading.Thread(name="checkUpdateStatus", target=checkUpdateStatus)
        checkUpdateStatusThread.start()
    elif Action == "startAchievementSystem":
        try:
            from win10toast_click import ToastNotifier
            toaster = ToastNotifier()
        except: return "ERROR-Package_Missing"
    elif Action == "apiSetup":
        import webbrowser, uuid
        webbrowser.open("https://home.openweathermap.org/users/sign_up",  new = 2, autoraise = True)
        print(clear() + "API Key Setup:\n\n\nTo use Oszust OS Storm Eye, you must create a free account on OpenWeatherMap.org.\nOur weather services use their API weather.\n\nThe following steps will walk you through how to create an account and get an API key.")
        print("\n\n1. Create an account at https://home.openweathermap.org/users/sign_up.\n(You can use a previsouly created account if you have one.)")
        print("\n2. After creating your account, click your username on the top right of the screen. Click 'My API Keys' from the dropdown menu.\n(Your username is the second from right button on the upper bar.)")
        print("\n3. In the 'Create Key' column, type 'Oszust OS Storm Eye' in the 'API key name' box. Click the generate button.")
        print("\n4. Copy the long key from under the key column to the input below. Press 'Enter' when done.\n\nNOTE: You must wait about five minutes for the key to register.")
        userAPIKey = input("\n\nYour API Key Here: ").lower().replace(" ", "")
        if os.path.isfile(appdata + systemName + "\\Config.json") == False:
            with open(appdata + systemName + "\\Config.json", 'w') as f: json.dump({}, f, indent=4)
        with open(appdata + systemName + "\\Config.json", 'r') as f:
            data = json.load(f)
            data["userAPIKey"] = userAPIKey
            tempfile = os.path.join(os.path.dirname(appdata + systemName + "\\Config.json"), str(uuid.uuid4()))
        with open(tempfile, 'w') as f: json.dump(data, f, indent=4)
        os.remove(appdata + systemName + "\\Config.json")
        os.rename(tempfile, appdata + systemName + "\\Config.json")
        softwareSetup()       

def checkUpdateStatus():
    global exitSystem
    ## Threading - Check Update Status
    import time, webbrowser
    while True:
        if AutoUpdater.UpdateStatus == 3:
            exitSystem = True
            exitText = input(clear() + "An emergency has been downloaded.\nThe update has fixed critical issues.\n\nPress any key to exit "+systemName+" and finish the installation...")
            exit()
        elif AutoUpdater.UpdateStatus in [1, 2]:
            toaster.show_toast(systemName + ": New Update Installed", "Relaunch the app to finish the installation.\n(Click to open the changelog.)", icon_path = str(Path(__file__).resolve().parent) + "\\DownloadIcon.ico", duration = 8, threaded = True, callback_on_click = openChangelog)
            return "Update Cleared"
        elif AutoUpdater.UpdateStatus == -3:
            toaster.show_toast(systemName + ": AutoUpdater Failed", "A requested app build does not exist.", icon_path = str(Path(__file__).resolve().parent) + "\\DownloadIcon.ico", duration = 8, threaded = True)
            return "Update Failed"
        elif AutoUpdater.UpdateStatus in [-2, 0]: return "Update Cleared"
        else: time.sleep(0.3)

def crashMessage():
    ## Display Crash
    global Argument
    import webbrowser
    webbrowser.open("https://github.com/Oszust-Industries/" + systemName.replace(" ", "-"),  new = 2, autoraise = True)
    print(clear() + "Crash Log:\n" + ("-" * 50 + "\n") + str(Argument) + ("\n" + "-" * 50) + "\n")
    crash = input(systemName + " has crashed. Please report your crash to the issues tab in GitHub.\n\nPress enter to restart " + systemName + "...\n")
    if crash not in ["exit()", "exit", "quit"]:
        try: softwareSetup()
        except Exception as Argument: crashMessage()
    else: exit()

def mainMenu():
    global recentSearches
    pickle.dump(recentSearches, open(appdata + systemName + "\\Recent.p", "wb"))
    menuSpot = 2
    favoriteSearches = []
    if "ALPHA" in softwareVersion: print(systemName + " " + softwareVersion + "\nCreated and published by Oszust Industries\n\n")
    else: print(systemName + " " + softwareVersion[:-4] + "\nCreated and published by Oszust Industries\n\n")
    print("1. Settings (To Be Added Soon)")
    print("\nFavorite Locations:")
    if len(favoriteSearches) == 0: print("No favorite locations yet.")
    else:
        favoriteSearches.sort()
        for i in favoriteSearches:
            print("   " + str(menuSpot) + ". " + i)
            menuSpot += 1
    print("\nRecent Searches:")
    if len(recentSearches) == 0: print("No recent searches.")
    else:
        for i in recentSearches:
            print("   " + str(menuSpot) + ". " + i)
            menuSpot += 1
    cityName = input("\nEnter city name or menu option: ").replace(" ", "+")
    if exitSystem == True: return
    if cityName.isnumeric() and int(cityName) >= 2 and int(cityName) < menuSpot:
        if int(cityName) > len(favoriteSearches): cityName = recentSearches[(int(cityName) - len(favoriteSearches)) - 2]
    if ",+" in cityName: cityName += ",+us"
    basicWeather(cityName.replace(" ", "+"))

def basicWeather(searchCityName):
    global hourly, recentSearches
    try:
        print("\nLoading Weather...")
        weatherData = json.loads(urlopen("http://api.openweathermap.org/data/2.5/weather?appid=" + apiKey + "&units=imperial&q=" + searchCityName).read())
        coord = weatherData["coord"]
        ForecastData = json.loads(urlopen("https://api.openweathermap.org/data/2.5/onecall?lat=" + str(coord["lat"]) + "&lon=" + str(coord["lon"]) + "&units=imperial&appid=" + apiKey).read())
        hourly = ForecastData["hourly"]
        main = weatherData["main"]
        coord = weatherData["coord"]
        sys = weatherData["sys"]
        cityName = weatherData["name"] + ", " + sys["country"]
        cityTemp =  int(main["temp"])
        cityFeelTemp = int(main["feels_like"])
        cityPressure = main["pressure"]
        cityWeatherDescription = weatherData["weather"][0]["description"]
        if cityName in recentSearches: recentSearches.remove(cityName)
        recentSearches.insert(0, cityName)
        if len(recentSearches) > 5: recentSearches.remove(recentSearches[5])
        cityHumidity = main["humidity"]
        timeZone = str([ s[0] for s in ((datetime.datetime.now().astimezone()).tzinfo).tzname((datetime.datetime.now()).astimezone()).split() ]).replace("'", "").replace("[", "").replace("]", "").replace(",", "").replace(" ", "")
        citySunset = datetime.datetime.fromtimestamp(weatherData["sys"]["sunset"]+60).strftime("%I:%M %p %Z%z") + timeZone
        citySunrise = datetime.datetime.fromtimestamp(weatherData["sys"]["sunrise"]+60).strftime("%I:%M %p %Z%z") + timeZone
        print(clear())
        print(str(cityName) + ":\n")
        if cityWeatherDescription[-1] == "s": print(str(cityTemp) + u"\N{DEGREE SIGN}" + " with " + str(cityWeatherDescription).capitalize())
        else: print(str(cityTemp) + u"\N{DEGREE SIGN}" + " with a " + str(cityWeatherDescription).capitalize())
        print("Feels: " + str(cityFeelTemp) + u"\N{DEGREE SIGN}")
        if int(hourly[1]["pop"] * 100) > 50 and int(hourly[1]["temp"]) > 32: print("\nRain during the next hour.")
        elif int(hourly[1]["pop"] * 100) > 50 and int(hourly[1]["temp"]) <= 32: print("\nSnow during the next hour.")
        else: print("\nNo precipitation during the next hour.")
        print("\nPressure: " + str(cityPressure) + " mbar")
        if citySunset[0] == "0": citySunset = citySunset[1:]
        if (datetime.datetime.now().hour < datetime.datetime.fromtimestamp(weatherData["sys"]["sunset"]).hour): print("Sunset: " + str(citySunset))
        elif (datetime.datetime.now().hour == datetime.datetime.fromtimestamp(weatherData["sys"]["sunset"]).hour) and (datetime.datetime.now().minute < datetime.datetime.fromtimestamp(weatherData["sys"]["sunset"]).minute): print("Sunset: " + str(citySunset))
        else: print("Sunrise: " + str(citySunrise))
        print("Moon: " + moonPosition(weatherData["sys"]["sunset"]+60) + "\n")
        weatherForecast(cityName)
    except: print(clear() + "The requested location could not be found.")
    print("\n\n\n")
    mainMenu()

def moonPosition(cityTime):
    import math, decimal, datetime
    dec = decimal.Decimal
    diff = datetime.datetime.fromtimestamp(cityTime) - datetime.datetime(2001, 1, 1)
    days = dec(diff.days) + (dec(diff.seconds) / dec(86400))
    lunations = dec("0.20439731") + (days * dec("0.03386319269"))
    index = math.floor((lunations % dec(1) * dec(8)) + dec("0.5"))
    return{0: "New Moon",1: "Waxing Crescent",2: "First Quarter",3: "Waxing Gibbous",4: "Full Moon",5: "Waning Gibbous",6: "Third Quarter",7: "Waning Crescent"}[int(index) & 7]

def weatherForecast(cityName):
    for i in range(1, 12):
        hourlyTime = datetime.datetime.fromtimestamp(hourly[i]["dt"]).strftime("%I:%M %p %Z%z")[:-1]
        date = (datetime.datetime.now()).strftime("%m/%d/%y")
        tomorrowDate = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m/%d/%y")
        if hourlyTime[0] == "0": hourlyTime = hourlyTime[1:]
        if date[0] == "0": date = date[1:]
        if tomorrowDate[0] == "0": tomorrowDate = tomorrowDate[1:]
        if i == 1: print("Hourly Forecast:")
        print("\t" + hourlyTime + ":")
        print("\t\tFeels-like Temperature: " + str(int(hourly[i]["feels_like"])) + u"\N{DEGREE SIGN}")
        print("\t\tPrecipitation Probability: " + str(int(hourly[i]["pop"] * 100)) + "%")
        if hourlyTime == "11:00 PM": print(("-" * 45) + "\n" + str(tomorrowDate) + ": (Sunrise/Sunset):")


## Start System
try: softwareSetup()
except Exception as Argument: crashMessage()
