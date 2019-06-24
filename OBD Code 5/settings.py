# Importing the required moduels
from pygame import init , image , font
from os import path

# Intialize pygame elements
init()

# Colors
black = (0,0,0)
green = (0,255,0)
white = (255,255,255)
red = (255,0,0)
gray = (140,140,140)
yellow = (255,211,0)
blue = (0,0,102)

# Fonts
propertyFont = font.Font("fonts\\OpenSans-BoldItalic.ttf",31)
valueFont = font.Font("fonts\\LemonMilk.otf",30)
alarmFont = font.Font("fonts\\LemonMilk.otf",25)
codeFont = font.Font("fonts\\LemonMilk.otf",23)
descFont = font.Font("fonts\\OpenSans-BoldItalic.ttf",22)
extraFont =font.Font("fonts\\OpenSans-BoldItalic.ttf",35)

# Images
logo = image.load("images\\logo\\finalLogo.png")
nxtArrow = image.load("images\\arrows\\next.png")
prvArrow = image.load("images\\arrows\\previous.png")
rtnButton = image.load("images\\buttons\\Return.png")
clrButton = image.load("images\\buttons\\Clear.png")
alert = image.load("images\\alarm\\alarm.jpg")
diagnostic = image.load("images\\diagno\\diagnostic.jpg")
title =image.load("images\\title\\obdTitle.png")


# load tach images
files_names = ['{}.png'.format(i) for i in range(0, 42)]
tach_images = [image.load(path.join("images\\tach\\",file)) for file in files_names]

# Display settings
Resolution = (800,480)
displayobj = None
screenNo = 0
dtcTabNo = 0
alarmNo = 0
showNo = 0

# Safe and Sound product
productID = 10

# car parameters
rpm = 0
o2MaxVolt = 0
o2MinVolt = 0
speed = 0
intakeTemp = 0
coolantTemp = 0
throttlePosition = 0
fuelRate = 0
ambiantTemp = 0
engineLoad = 0
runTime = 0
refDistance = 0
distance = 0
oilTemp = 0
maf = 0
dtc = []
dtcNo = 0
newDtcs = []
o2SenReadings = []

# ECU Simulator
dataSet = []
snapShoot = 1

# Flags
normal_state = True
check_state = False
ecuReady = False
Diagnostic_ass = False
Alarm_sys = False
intakeAlarm = False
mafAlarm = False
coolantAlarm = False
oilAlarm = False
o2Alarm = False
fuelAlarm = False
tripFlag = True
stopSystemTimer = False
movingFlag = False
logFlag = False

# Timers
system_timer = 0
log_timer = 0
highCoolantTemp_timer = 0
apnormalOilTemp_timer = 0
intakeSenFailure_timer = 0
fuelEconomy_timer = 0
o2SenFailure_timer = 0
o2SenSlot = 0
timeSlot = 0
simulationSlot = 0

# Counters
system_counter = 0
coolantTemp_counter = 0
oilTemp_counter = 0
fuelEconomy_counter = 0
mafSenFailure_counter = 0
o2SenFailure_counter = 0
trip_counter = 1200

# Alarm system
alarmNo = 0
totalCoolantTemp = 0
totalOilTemp = 0
totalSpeed = 0
totalFuelRate = 0
totalMaf = 0
totalRpm = 0
totalRpmSequare = 0
totalRpmInMaf = 0
totalMaxVoltage = 0
totalMinVoltage = 0

# Trip details
accountID = 1
tripID = None
tripStartTime = None
tripTotalSpeed = 0
tripTotalFuelRate = 0
timeBeforeMoving = 0


