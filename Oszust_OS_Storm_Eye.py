## Oszust OS Storm Eye - Oszust Industries
## Created on: 12-16-21 - Last update: 3-12-21
softwareVersion = "ALPHA-v1.0.0.007"
def clear(): return ("\n" * 70)
from urllib.request import urlopen
from pathlib import Path
import threading, datetime, json, os
import AutoUpdater

def softwareConfig():
    import uuid
    ## System Configuration
    global appBuild, appdata, deactivateFileOpening, exitSystem, resetSettings, systemName, MeasurementUnits, HourlyForecastScale, apiKey
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

def softwareSetup():
    ## Setup Software
    global accountReady, restartNeed, deactivateFileOpening
    print("Loading...")
    softwareConfig()
    serverActions("wifiTest")
    serverActions("startAchievementSystem")
    AutoUpdater.setupUpdate(systemName, appBuild, softwareVersion)
    serverActions("updateStatusCheckThreadStart")
    if apiKey == "":
        serverActions("apiSetup")
        return
    ## Start Functions
    if exitSystem == False:
        if os.name != "nt": deactivateFileOpening = True  ## Windows Detector
        print(clear() + "Welcome to " + systemName + ". " + softwareVersion[:-4] + "\nCreated and published by Oszust Industries\n\n")
        basicWeather()

def serverActions(Action):
    global exitSystem, toaster, userAPIKey
    if Action == "wifiTest":
        from urllib.request import urlopen
        try: urlopen("http://google.com", timeout=1)
        except: serverActions("noWifi")
    elif Action == "noWifi":
        import random
        print(clear() + "There doesn't seem to be any internet connection on your device.\n" + systemName + " needs internet to display the weather.\n")
        retry = input("\"" + random.choice(open("./Wifi text.txt").read().splitlines()) + "\"\n\nPress 'Enter' to retry the internet connection...")
        print(clear())
        softwareSetup()
    elif Action == "updateStatusCheckThreadStart":
        checkUpdateStatusThread = threading.Thread(name="checkUpdateStatus", target=checkUpdateStatus)
        checkUpdateStatusThread.start()
    elif Action == "startAchievementSystem":
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
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
    ## Threading - Check Update Status
    import time
    while True:
        if AutoUpdater.UpdateStatus == 3:
            print(clear() + "An emergency has been downloaded.\nThe update has fixed critical issues.\n\nPlease restart "+systemName+" to finish the installation.")
            exit()
        elif AutoUpdater.UpdateStatus in [1, 2]:
            toaster.show_toast(systemName + ": New Update Installed", "Relaunch the app to finish the update.", icon_path = str(Path(__file__).resolve().parent) + "\\DownloadIcon.ico", duration = 8, threaded = True)
            return "Update Cleared"
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

def basicWeather():
    searchCityName = input("Enter city name: ").replace(" ", "+")
    if ",+" in searchCityName: searchCityName += ",+us"
    try:
        weatherData = json.loads(urlopen("http://api.openweathermap.org/data/2.5/weather?appid=" + apiKey + "&units=imperial&q=" + searchCityName).read())
        print("Loading Weather...")
        main = weatherData["main"]
        coord = weatherData["coord"]
        sys = weatherData["sys"]
        cityName = weatherData["name"] + ", " + sys["country"]
        cityTemp =  int(main["temp"])
        cityFeelTemp = int(main["feels_like"])
        cityPressure = main["pressure"]
        cityWeatherDescription = weatherData["weather"][0]["description"]

        cityHumidity = main["humidity"]
        timeZone = str([ s[0] for s in ((datetime.datetime.now().astimezone()).tzinfo).tzname((datetime.datetime.now()).astimezone()).split() ]).replace("'", "").replace("[", "").replace("]", "").replace(",", "").replace(" ", "")
        citySunset = datetime.datetime.fromtimestamp(weatherData["sys"]["sunset"]+60).strftime("%I:%M %p %Z%z") + timeZone
        citySunrise = datetime.datetime.fromtimestamp(weatherData["sys"]["sunrise"]+60).strftime("%I:%M %p %Z%z") + timeZone
        print(clear())
        print("\n\n\nCurrent Weather in "+ str(cityName) + ":\n")
        print("Temperature: " + str(cityTemp) + u"\N{DEGREE SIGN}")
        print("Feels-like Temperature: " + str(cityFeelTemp) + u"\N{DEGREE SIGN}")
        print("Pressure: " + str(cityPressure) + " mbar")
        if (datetime.datetime.now().hour < datetime.datetime.fromtimestamp(weatherData["sys"]["sunset"]).hour): print("Sunset: " + str(citySunset))
        elif (datetime.datetime.now().hour == datetime.datetime.fromtimestamp(weatherData["sys"]["sunset"]).hour) and (datetime.datetime.now().minute < datetime.datetime.fromtimestamp(weatherData["sys"]["sunset"]).minute): print("Sunset: " + str(citySunset))
        else: print("Sunrise: " + str(citySunrise))
        print("Weather Description: " + str(cityWeatherDescription))
        print("Moon: " + moonPosition(weatherData["sys"]["sunset"]+60) + "\n\n\n")
        weatherForecast(str(coord["lon"]), str(coord["lat"]), cityName)
    except: print("City Not Found")
    print("\n\n\n")
    basicWeather()

def moonPosition(cityTime):
    import math, decimal, datetime
    dec = decimal.Decimal
    diff = datetime.datetime.fromtimestamp(cityTime) - datetime.datetime(2001, 1, 1)
    days = dec(diff.days) + (dec(diff.seconds) / dec(86400))
    lunations = dec("0.20439731") + (days * dec("0.03386319269"))
    index = math.floor((lunations % dec(1) * dec(8)) + dec("0.5"))
    return{
      0: "New Moon", 
      1: "Waxing Crescent", 
      2: "First Quarter", 
      3: "Waxing Gibbous", 
      4: "Full Moon", 
      5: "Waning Gibbous", 
      6: "Third Quarter", 
      7: "Waning Crescent"
    }[int(index) & 7]

def weatherForecast(cityLon, cityLat, cityName):
    ForecastData = json.loads(urlopen("https://api.openweathermap.org/data/2.5/onecall?lat=" + cityLat + "&lon=" + cityLon + "&units=imperial&appid=" + apiKey).read())
    hourly = ForecastData["hourly"]
    print("Hourly Forecast for " + cityName + ":\n")
    for i in range(1, 12):
        hourlyTime = datetime.datetime.fromtimestamp(hourly[i]["dt"]).strftime("%I:%M %p %Z%z")[:-1]
        if hourlyTime[0] == "0": hourlyTime = hourlyTime[1:]
        if i == 1 and hourlyTime != "11:00 PM": print(str((datetime.datetime.now()).strftime("%m/%d/%y")) + ":")
        print("\t" + hourlyTime + ":")
        print("\t\tFeels-like Temperature: " + str(int(hourly[i]["feels_like"])) + u"\N{DEGREE SIGN}")
        print("\t\tPrecipitation Probability: " + str(int(hourly[i]["pop"] * 100)) + "%")
        if hourlyTime == "11:00 PM": print(("-" * 45) + "\n" + str((datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m/%d/%y")) + ":")


## Start System
try: softwareSetup()
except Exception as Argument: crashMessage()
