import json, sys, time, os

def errorMessage(msg):
  print(f"\rAn invalid {msg} was chosen.")
  time.sleep(1)
  sys.stdout.write("\033[F") # Cursor up one line
  sys.stdout.write("\033[K") # Clears to end of line

def errorMessageNum(msg, numMsg):
  print(f"\rThe input was too {msg}. Please let the value be {numMsg}.")
  time.sleep(1)
  sys.stdout.write("\033[F") # Cursor up one line
  sys.stdout.write("\033[K") # Clears to end of line

def writeJSON(name, value):
  data = {}

  # reads the content in the config.json file
  with open('resources/config.json', 'r') as fp:
    data = json.load(fp)

    data[name] = value # Updates new value in data
  
  # writes new data in the config.json file
  with open('resources/config.json', 'w') as fp:
    json.dump(data, fp, indent=4)
  
  # Makes JSON data more readible
  data_print = json.dumps(data, indent=4)
  print(data_print)

def changePath():
  os.system('cls' if os.name == 'nt' else 'clear')
  print("What is your path to the league client? (leave empty to not change path)")
  validInput = False
  while not (validInput):
    userInput = input(">> ")
    if userInput == "":
      print("The path will not be changed.")
      validInput = True
    elif userInput.isnumeric():
      errorMessage("integer")
    else:
      writeJSON('client path', userInput)
      print("The path was changed succesfully.")
      print(f"Path: {userInput}")
      time.sleep(2)
      validInput = True

def changeLoginSpeed():
  os.system('cls' if os.name == 'nt' else 'clear')
  loginSpeed = 0

  with open('resources/config.json', 'r') as fp:
    data = json.load(fp)
    loginSpeed = data['login speed']

  print(f"What login speed do you wish to have? Current: {loginSpeed}")
  validInput = False
  while not (validInput):
    userInput = input("(num) >> ")
    if not userInput.isnumeric():
      errorMessage("input")
    else:
      if int(userInput) > 10:
        errorMessageNum("high", "10 or below")
      elif int(userInput) <= 0:
        errorMessageNum("low", "higher than 0 secs")
      else:
        writeJSON('login speed', userInput)
        print("The login speed was changed succesfully.")
        print(f"new login speed: {userInput}")
        time.sleep(2)
        validInput = True
    
validInput = False
while not (validInput):
  validInput = True
  print('''What do you want to configure?
  1: change path
  2: change login speed
  ''')
  userInput = input("(num) >> ")
  if userInput.isnumeric():
    if int(userInput) is 1:
      changePath()
    elif int(userInput) is 2:
      changeLoginSpeed()
    else:
      errorMessage("integer")
      validInput = False
  else:
    errorMessage("input")
    validInput = False
  