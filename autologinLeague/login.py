import os, subprocess, sys, time, platform, json, psutil, pathlib
from pynput.keyboard import Key, Controller

userOS = platform.system()
loginInfo = {'Username': None, 'Password': None}
absPath = pathlib.Path(__file__).parent.absolute() # gives absolute path
os.chdir(absPath) # puts working path to absolute path

# displays error message if invalid input
def errorMessage(msg):
  print(f"\rAn invalid {msg} was chosen.")
  time.sleep(1)
  sys.stdout.write("\033[F") # Cursor up one line
  sys.stdout.write("\033[K") # Clears to end of line

# reads summoner name in loginInfo.txt and asks user to choose account
# prompts for choosing existing account in loginInfo.txt
# skips prompt (choosing stage), if only one account is inserted in the app
def chooseAccount():
  # reads the file line by line
  with open("loginInfo.txt", "r") as fp:
    Lines = fp.readlines()
    accountCount = 0 # requires another variable in function scope and not for loop scope

    # prints first element of text string (in-game name)
    for count, line in enumerate(Lines):
      accountName = line.split()[0]
      print(count, accountName)
      accountCount += 1

    if(accountCount == 0):
      print("You have not typed an account into the loginInfo.txt file. Please follow the instructions for help.")
      time.sleep(5)
      sys.exit()

    if(accountCount == 1):
      print("A valid account was chosen.")
      loginInfo['Username'] = line.split()[1]
      loginInfo['Password'] = line.split()[2]
      validInput = True
      return # stop function 

    # asks the user for input
    print("Which account do you want to use?")

    # user types input and repeats if not satisfied
    # either through int or string format
    validInput = False
    while(not validInput):
      userInput = input(">> ")
      if userInput.isnumeric():
        userInput = int(userInput)
        if userInput >= 0 and userInput <= count:
          print("A valid account was chosen.")
          for count, line in enumerate(Lines):
            if count == userInput:
              loginInfo['Username'] = line.split()[1]
              loginInfo['Password'] = line.split()[2]
              validInput = True
              break 
        else:
          errorMessage("number")
      elif type(userInput) == str:
        for line in Lines:
          accountName = line.split()[0]
          if userInput == accountName:
            print("A valid account was chosen.")
            loginInfo['Username'] = line.split()[1]
            loginInfo['Password'] = line.split()[2]
            validInput = True
            break
        else:
          errorMessage("string")   
      else:
        #Should not happen as any input should either be int or string
        errorMessage("input")

# changes path to standard download paths if not set up, then opens league
def openClient():
  # finds operating system

  data = {}
  clientPath = ""

  # Initializes standard download path for league client. 
  # Goto setup.py to change manually if not working
  with open('resources/config.json', 'r') as fp:
    data = json.load(fp)
    clientPath = data['client path']
    if (clientPath == ""):
      if (userOS == "Darwin"):
        data['client path'] = '/Applications/League of Legends.app/Contents/LoL/LeagueClient.app'
      elif (userOS == "Windows"):
        data['client path'] = 'C:\Riot Games\League of Legends\LeagueClient.exe'
      else:
        sys.exit("Your operating system is not supported for this application")
    clientPath = data['client path']

  # ups file path in config.json
  with open('resources/config.json', 'w') as fp:
    json.dump(data, fp, indent=4)


  # Opens the League Client with the relevant operating system and path
  if (userOS == "Darwin"):
      subprocess.call(['open', clientPath])
  elif (userOS == "Windows"):
      subprocess.call([clientPath])
  else:
      sys.exit("Your operating system is not supported for this application")

# returns true if the process name of the client exists
# meaning: checking if the app is open
def process_exists(process_name):
  return process_name in (p.name() for p in psutil.process_iter())

# waits until app is opened
def waitAppOpened():
  processName = ""
  loginSpeed = 2

  with open('resources/config.json', 'r') as fp:
    data = json.load(fp)
    if data['login speed'] != "2":
      loginSpeed = int(data['login speed'])

  if (userOS == "Darwin"):
    processName = "RiotClientUx"
    while not process_exists(processName):
      time.sleep(loginSpeed)
    time.sleep(2)
  elif (userOS == "Windows"):
    processName = "RiotClientServices.exe"
    while not process_exists(processName):
      time.sleep(loginSpeed)

# types in the login information into the league client
def typeLogin():
  Username = loginInfo['Username']
  Password = loginInfo['Password']

  # controls keyboard keys
  keyboard = Controller()

  keyboard.type(Username)
  keyboard.press(Key.tab)
  keyboard.type(Password)

  time.sleep(.2) # gives time for loginInfo to be typed

  keyboard.press(Key.enter)
  keyboard.release(Key.enter)

chooseAccount()
openClient()
waitAppOpened()
typeLogin()

os.system('cls' if os.name == 'nt' else 'clear') # just making sure it is clear after use
sys.exit() # quits program when everything is typed
