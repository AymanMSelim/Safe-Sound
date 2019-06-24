# importing the required elements
import settings , obd ,  csv , MySQLdb 
from random import randint
from math import ceil
from datetime import datetime
from threading import Timer

# helper function to display different texts on the screen
def display_text(string , x ,y , Type):
    if (Type == "property" and settings.normal_state) :
        text = settings.propertyFont.render(string,True,settings.white)
    elif(Type == "property" and settings.check_state):
        text = settings.propertyFont.render(string,True,settings.yellow)
    elif Type == "value" :
        text = settings.valueFont.render(string,True,settings.green)
    elif Type == "alarmOn" :
        text = settings.alarmFont.render(string,True,settings.red)
    elif Type == "alarmOff" :
        text = settings.alarmFont.render(string,True,settings.gray)
    elif (Type == "extra" and settings.Alarm_sys) :
        text = settings.extraFont.render(string,True,settings.yellow)
    elif (Type == "extra" and settings.Diagnostic_ass):
        text = settings.extraFont.render(string,True,settings.blue)
    textRect = text.get_rect()
    textRect.centerx = settings.displayObj.get_rect().centerx+x
    textRect.centery = settings.displayObj.get_rect().centery+y
    settings.displayObj.blit(text,textRect)

# helper function to drwa DTCs
def display_DTC(string , x , y , Type):
    if (Type == "code" and (not settings.Diagnostic_ass)) :
        text = settings.codeFont.render(string,True,settings.green)
    elif (Type == "code" and settings.Diagnostic_ass ):
        text = settings.codeFont.render(string,True,settings.red)
    elif (Type == "desc" and ( not settings.Diagnostic_ass)) :
        text = settings.descFont.render(string,True,settings.white)
    elif (Type == "desc" and settings.Diagnostic_ass) :
        text = settings.descFont.render(string,True,settings.black)
    settings.displayObj.blit(text,(x,y))

# helper function to display images on the screen
def display_image(image,x,y):
    settings.displayObj.blit(image,(x,y))

# helper function to turn over screens
def set_screenNo(action):
    if action == "inc" :
        settings.screenNo += 1
        if settings.screenNo > 2 :
            settings.screenNo = 0
    elif action == "dec" :
        settings.screenNo -= 1
        if settings.screenNo < 0 :
            settings.screenNo = 2

# helper function to turn over DTC tabs
def set_dtcTabNo():
    no_of_tabs = ceil(len(settings.dtc)/6)
    if(settings.dtcTabNo < no_of_tabs - 1):
        settings.dtcTabNo +=1
    else:
        settings.dtcTabNo = 0

# helper function produces different timers
def runTimers():
    t = Timer(.5, runTimers)
    t.start()
    settings.system_timer += .5
    settings.log_timer += .5
    settings.timeSlot += .5
    settings.simulationSlot += .5
    if(settings.simulationSlot >= 1):
        settings.simulationSlot = 0
        setCarParameters()
        generateRand()
    if(settings.timeSlot >= 2):
        settings.timeSlot = 0
    if (settings.system_timer >= 60):
        settings.system_timer = 0
        settings.highCoolantTemp_timer += 1
        settings.apnormalOilTemp_timer += 1
        settings.intakeSenFailure_timer += 1
        settings.fuelEconomy_timer += 1
        if(settings.tripFlag):
            settings.o2SenFailure_timer +=1
    if (settings.stopSystemTimer):
        t.cancel()
            

# Function to figure out what tach image we should display based on the RPM.
def getTach1():
	rpm = settings.rpm
	tach_iter = 0
	if rpm == 0:
		tach_iter = 0
	elif (rpm >= 0) & (rpm < 200):
		tach_iter = 1
	elif (rpm >= 200) & (rpm < 400):
		tach_iter = 2
	elif (rpm >= 400) & (rpm < 600):
		tach_iter = 3
	elif (rpm >= 600) & (rpm < 800):
		tach_iter = 4
	elif (rpm >= 800) & (rpm < 1000):
		tach_iter = 5
	elif (rpm >= 1000) & (rpm < 1200):
		tach_iter = 6
	elif (rpm >= 1200) & (rpm < 1400):
		tach_iter = 7
	elif (rpm >= 1400) & (rpm < 1600):
		tach_iter = 8
	elif (rpm >= 1600) & (rpm < 1800):
		tach_iter = 9
	elif (rpm >= 1800) & (rpm < 2000):
		tach_iter = 10
	elif (rpm >= 2000) & (rpm < 2200):
		tach_iter = 11
	elif (rpm >= 2200) & (rpm < 2400):
		tach_iter = 12
	elif (rpm >= 2400) & (rpm < 2600):
		tach_iter = 13
	elif (rpm >= 2600) & (rpm < 2800):
		tach_iter = 14
	elif (rpm >=2800) & (rpm < 3000):
		tach_iter = 15
	elif (rpm >= 3000) & (rpm < 3200):
		tach_iter = 16
	elif (rpm >= 3200) & (rpm < 3400):
		tach_iter = 17
	elif (rpm >= 3400) & (rpm < 3600):
		tach_iter = 18
	elif (rpm >= 3600) & (rpm < 3800):
		tach_iter = 19
	elif (rpm >= 3800) & (rpm < 4000):
		tach_iter = 20
	elif (rpm >= 4000) & (rpm < 4200):
		tach_iter = 21
	elif (rpm >= 4200) & (rpm < 4400):
		tach_iter = 22
	elif (rpm >= 4400) & (rpm < 4600):
		tach_iter = 23
	elif (rpm >= 4600) & (rpm < 4800):
		tach_iter = 24
	elif (rpm >= 4800) & (rpm < 5000):
		tach_iter = 25
	elif (rpm >= 5000) & (rpm < 5200):
		tach_iter = 26
	elif (rpm >= 5200) & (rpm < 5400):
		tach_iter = 27
	elif (rpm >= 5400) & (rpm < 5600):
		tach_iter = 28
	elif (rpm >= 5600) & (rpm < 5800):
		tach_iter = 29
	elif (rpm >= 5800) & (rpm < 6000):
		tach_iter = 30
	elif (rpm >= 6000) & (rpm < 6200):
		tach_iter = 31
	elif (rpm >= 6200) & (rpm < 6400):
		tach_iter = 32
	elif (rpm >= 6400) & (rpm < 6600):
		tach_iter = 33
	elif (rpm >= 6600) & (rpm < 6800):
		tach_iter = 34
	elif (rpm >= 6800) & (rpm < 7000):
		tach_iter = 35
	elif (rpm >= 7000) & (rpm < 7200):
		tach_iter = 36
	elif (rpm >= 7200) & (rpm < 7400):
		tach_iter = 37
	elif (rpm >= 7400) & (rpm < 7600):
		tach_iter = 38
	elif (rpm >= 7600) & (rpm < 7800):
		tach_iter = 39
	elif (rpm >= 7800) & (rpm < 8000):
		tach_iter = 40
	elif (rpm >= 8000):
		tach_iter = 41
	return tach_iter

# Function to figure out what tach image we should display based on the speed.
def getTach2():
	speed = settings.speed
	tach_iter = 0
	if speed == 0:
		tach_iter = 0
	elif (speed >= 0) & (speed < 6):
		tach_iter = 1
	elif (speed >= 6) & (speed < 12):
		tach_iter = 2
	elif (speed >= 12) & (speed < 18):
		tach_iter = 3
	elif (speed >= 18) & (speed < 24):
		tach_iter = 4
	elif (speed >= 24) & (speed < 30):
		tach_iter = 5
	elif (speed >= 30) & (speed < 36):
		tach_iter = 6
	elif (speed >= 36) & (speed < 42):
		tach_iter = 7
	elif (speed >= 42) & (speed < 48):
		tach_iter = 8
	elif (speed >= 48) & (speed < 52):
		tach_iter = 9
	elif (speed >= 52) & (speed < 58):
		tach_iter = 10
	elif (speed >= 58) & (speed < 64):
		tach_iter = 11
	elif (speed >= 64) & (speed < 70):
		tach_iter = 12
	elif (speed >= 70) & (speed < 76):
		tach_iter = 13
	elif (speed >= 76) & (speed < 82):
		tach_iter = 14
	elif (speed >=82) & (speed < 88):
		tach_iter = 15
	elif (speed >= 88) & (speed < 94):
		tach_iter = 16
	elif (speed >= 94) & (speed < 100):
		tach_iter = 17
	elif (speed >= 100) & (speed < 106):
		tach_iter = 18
	elif (speed >= 106) & (speed < 112):
		tach_iter = 19
	elif (speed >= 112) & (speed < 118):
		tach_iter = 20
	elif (speed >= 118) & (speed < 124):
		tach_iter = 21
	elif (speed >= 124) & (speed < 130):
		tach_iter = 22
	elif (speed >= 130) & (speed < 136):
		tach_iter = 23
	elif (speed >= 136) & (speed < 142):
		tach_iter = 24
	elif (speed >= 142) & (speed < 148):
		tach_iter = 25
	elif (speed >= 148) & (speed < 154):
		tach_iter = 26
	elif (speed >= 154) & (speed < 160):
		tach_iter = 27
	elif (speed >= 160) & (speed < 166):
		tach_iter = 28
	elif (speed >= 166) & (speed < 172):
		tach_iter = 29
	elif (speed >= 172) & (speed < 178):
		tach_iter = 30
	elif (speed >= 178) & (speed < 184):
		tach_iter = 31
	elif (speed >= 184) & (speed < 190):
		tach_iter = 32
	elif (speed >= 190) & (speed < 196):
		tach_iter = 33
	elif (speed >= 196) & (speed < 202):
		tach_iter = 34
	elif (speed >= 202) & (speed < 208):
		tach_iter = 35
	elif (speed >= 208) & (speed < 214):
		tach_iter = 36
	elif (speed >= 214) & (speed< 220):
		tach_iter = 37
	elif (speed >= 220) & (speed < 226):
		tach_iter = 38
	elif (speed >= 226) & (speed < 232):
		tach_iter = 39
	elif (speed >= 232) & (speed < 236):
		tach_iter = 40
	elif (speed >= 236):
		tach_iter = 41
	return tach_iter

# helper function that detects if there are new DTCs found
def new_DTCs():
    if(len(settings.dtc) > settings.dtcNo):
        settings.newDtcs = settings.dtc[settings.dtcNo:]
        settings.Diagnostic_ass = True
    settings.dtcNo = len(settings.dtc)

# helper function that generates high coolant temperature alarm
def highCoolantTemAlarm():
    average = 0
    if(settings.timeSlot >= 1.5):
        settings.totalCoolantTemp += settings.coolantTemp
        settings.coolantTemp_counter += 1
    if(settings.highCoolantTemp_timer >= 2):
        average = settings.totalCoolantTemp / settings.coolantTemp_counter
        settings.totalCoolantTemp = 0
        settings.coolantTemp_counter = 0
        settings.highCoolantTemp_timer = 0
        if(average >=  104):
            settings.Alarm_sys = True
            settings.alarmNo = 4
            settings.coolantAlarm = True
        else:
            settings.coolantAlarm = False

# helper function that generates apnormal oil temperature alarm
def apnormalOilTempAlarm():
    average = 0
    if(settings.timeSlot >= 1.5):
        settings.totalOilTemp += settings.oilTemp
        settings.oilTemp_counter += 1
    if(settings.apnormalOilTemp_timer >= 2):
        average = settings.totalOilTemp / settings.oilTemp_counter
        settings.totalOilTemp = 0
        settings.oilTemp_counter = 0
        settings.apnormalOilTemp_timer = 0
        if(average >= 104 or average <= 60 ):
            settings.Alarm_sys = True
            settings.alarmNo = 5
            settings.oilAlarm = True
        else:
            settings.oilAlarm = False

# helper function that generates intake sensor faiure alarm
def intakeSensorFailureAlarm():
    if(settings.intakeSenFailure_timer >= 5):
        difference = settings.intakeTemp - settings.ambiantTemp
        settings.intakeSenFailure_timer = 0
        if(difference >= 30):
            settings.Alarm_sys = True
            settings.alarmNo = 3
            settings.intakeAlarm = True
        else:
            settings.intakeAlarm = False

# helper function that generates low fuel economy alarm
def fuelEconomyAlarm():
    if(settings.timeSlot >= 1.5):
        settings.totalFuelRate += settings.fuelRate
        settings.totalSpeed += settings.speed
        settings.fuelEconomy_counter += 1
    if(settings.fuelEconomy_timer == 5):
        avgSpeed = settings.totalSpeed / settings.fuelEconomy_counter
        avgFuelRate = settings.totalFuelRate / settings.fuelEconomy_counter
        FuelEconomy = avgSpeed / avgFuelRate
        settings.totalSpeed = 0
        settings.totalFuelRate =0
        settings.fuelEconomy_counter =0
        settings.fuelEconomy_timer = 0
        if(FuelEconomy < 100):
            settings.Alarm_sys = True
            settings.alarmNo = 6
            settings.fuelAlarm = True
        else:
            settings.fuelAlarm = False

# helper function that generates MAF sensor failure alarm
def MAfSensorFailureAlarm():
    if(settings.timeSlot >= 1.5):
        settings.totalRpm += settings.rpm
        settings.totalMaf += settings.maf
        settings.totalRpmSequare += pow(settings.rpm,2)
        settings.totalRpmInMaf += settings.rpm * settings.maf
        settings.mafSenFailure_counter += 1
    if(settings.mafSenFailure_counter >= 300):
        x = settings.totalRpm
        y = settings.totalMaf
        z = settings.totalRpmSequare
        w = settings.totalRpmInMaf
        n = settings.mafSenFailure_counter
        newGrad = ((n * w) - (x * y)) /((n * z) - (x * x))
        f = open("MafSenFailure.txt","r")
        lastGrad = float(f.read())
        f = open("MafSenFailure.txt","w")
        f.write(str(newGrad))
        f.close()
        settings.mafSenFailure_counter = 0
        settings.tripFlag = False
        if((newGrad/lastGrad) < .7):
            settings.Alarm_sys = True
            settings.alarmNo = 1
            settings.mafAlarm = True
        else:
            settings.mafAlarm = False

# helper function that generates oxsgen sensor failure alarm
def o2SensorFaliureAlarm():
    settings.o2SenReadings.append(settings.o2Volt)
    if(settings.o2SenSlot >= 3):
        settings.o2SenSlot = 0
        settings.totalMaxVoltage += max(settings.o2SenReadings)
        settings.totalMinVoltage += min(settings.o2SenReadings)   
        settings.o2SenFailure_counter += 1
        settings.o2SenReadings = []
    if(settings.o2SenFailure_timer >= 15):
        avgMaxVolt = settings.totalMaxVoltage / settings.o2SenFailure_counter
        avgMinVolt = settings.totalMinVoltage / settings.o2SenFailure_counter
        settings.totalMaxVoltage = 0
        settings.totalMinVoltage = 0
        settings.o2SenFailure_counter = 0
        settings.o2SenFailure_interval = 0
        settings.tripFlag = False
        if(avgMaxVolt <= .6 or avgMinVolt >= .38):
            settings.Alarm_sys = True
            settings.alarmNo = 2
            settings.o2Alarm = True
        else:
            settings.o2Alarm = False
            
               
# helper function that calculates car moving distance
def getRefDistance():
    ports = obd.scan_serial()
    connection = obd.OBD(ports[0])
    r = connection.query(obd.commands.DISTANCE_SINCE_DTC_CLEAR)
    settings.refDistance = round(r.value.magnitude,2)
    connection.close()
    
# helper function that creates new log file with specified header
def createLogFile(header , fileName):
    with open('logs/' + fileName + '.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(header)

# helper function that logs car data into a specified log file
def logCarData(fileName):
    t = Timer(1,logCarData,(fileName,))
    t.start()
    data = [str(settings.runTime),str(settings.rpm),str(settings.speed),str(settings.coolantTemp),
            str(settings.intakeTemp),str(settings.maf),str(settings.throttlePosition),
            str(settings.engineLoad),str(settings.fuelRate),str(settings.oilTemp),str(settings.ambiantTemp)]
    with open('logs/' + fileName + '.csv', 'a') as f:
        w = csv.writer(f)
        w.writerow(data)
    if( settings.stopSystemTimer):
        t.cancel()

    
# helper function that reads a specfied log file 
def readLogFile(logFile):
    with open(logFile , "r") as f :
        reader = csv.reader(f)
        settings.dataSet = list(reader)
     
# helper function that simulates car ECU 
def setCarParameters():
    settings.rpm = int(settings.dataSet[settings.snapShoot][1])
    settings.speed = int(int(settings.dataSet[settings.snapShoot][2]) * 1.60934)
    settings.coolantTemp = int(settings.dataSet[settings.snapShoot][3])
    settings.intakeTemp = int(settings.dataSet[settings.snapShoot][4])
    settings.maf = round(float(settings.dataSet[settings.snapShoot][5]),2)
    settings.throttlePosition = int(settings.dataSet[settings.snapShoot][6])
    settings.engineLoad = int(settings.dataSet[settings.snapShoot][7])
    settings.fuelRate = float(settings.dataSet[settings.snapShoot][8])
    settings.ambiantTemp = int(settings.dataSet[settings.snapShoot][9])
    settings.snapShoot += 1
    if (settings.snapShoot == 2000):
        t.cancel()

# helper function that sets car variables by random values
def generateRand():
    settings.runTime = round(settings.runTime + (1/60) , 2) 
    settings.distance =  round(settings.distance + (settings.speed /(60*60)) , 2)
    settings.oilTemp = settings.coolantTemp + randint(12,15)
    #settings.coolantTemp = randint(110,150)
    #settings.maf = randint(0,30)
    #settings.rpm = randint(300,3000)
    #settings.fuelRate = randint(1,10)
    #settings.speed = randint(10,200)
    #settins.ambiantTemp = randint(28,32)
    #settings.intakeTemp = randint(30,45)

# helper function that logs start of new trip
def startNewTrip(startTime , date):
    db = MySQLdb.connect(host="192.168.43.187" , user="root", passwd="root12345", db="mydb")
    cur = db.cursor()
    sql = ("""INSERT INTO trip_t(StartTime,Date,ACCOUNT_T_AccountID) VALUES (%s,%s,%s)""", (startTime,date,settings.accountID))
    try:
        cur.execute(*sql)
        db.commit()
        print("Write complete")
        settings.logFlag = True
    except Exception as e:
        db.rollback()
        print ("Error: ",e)
    settings.tripID = cur.lastrowid
    cur.close()
    db.close()

# helper function that sets trip parameters
def tripCalculations():
    if(settings.timeSlot >= 1.5):
        settings.tripTotalSpeed += settings.speed
        settings.tripTotalFuelRate += settings.fuelRate
        settings.trip_counter += 1

#helper function that sets trip details
def setTripDetails():
    x = datetime.today()
    endTime = str(x.hour)+":"+str(x.minute)+":"+str(x.second)
    avgSpeed = settings.tripTotalSpeed / settings.trip_counter
    duration = settings.runTime - settings.timeBeforeMoving
    distance = settings.distance
    consumedLiters = (settings.tripTotalFuelRate/settings.trip_counter) * (duration/60)
    db = MySQLdb.connect(host="192.168.43.187" , user="root", passwd="root12345", db="mydb")
    cur = db.cursor()
    values = (endTime,avgSpeed,duration,distance,consumedLiters,settings.tripID)
    sql = ("""UPDATE trip_t SET EndTime = %s , AvgSpeed = %s , TripInterval = %s ,
              Distance = %s , ConsumedLiters = %s WHERE TripID = %s """,values )
    try:
        cur.execute(*sql)
        db.commit()
        print("Write complete")
    except Exception as e:
        db.rollback()
        print ("Error: ",e)
    cur.close()
    db.close()


# helper function that logs car data into database
def logSystem():
    db = MySQLdb.connect(host="192.168.43.187" , user="root", passwd="root12345", db="mydb")
    cur = db.cursor()
    x = datetime.today()
    currentDate = str(x.day)+"-"+str(x.month)+"-"+str(x.year)
    currentTime = str(x.hour)+":"+str(x.minute)+":"+str(x.second)
    values = (settings.coolantTemp,settings.intakeTemp,settings.oilTemp,settings.engineLoad,
                settings.throttlePosition,settings.speed,settings.rpm,settings.runTime,settings.distance,
                settings.maf,settings.fuelRate, currentDate , currentTime, settings.productID)   
    sql = ("""UPDATE obd_t SET CoolantTemp = %s , IntakeAirTemp = %s , OilTemp = %s , LoadEngine = %s , ThrottlePosition = %s , Speed = %s, RPM = %s ,RunTime = %s ,Distance = %s ,MAF = %s ,FuelRate = %s , Date = %s , Time = %s WHERE PRODUCT_T_ProductID = %s """,values)

    try:
        cur.execute(*sql)
        db.commit()
        print("Write complete")
    except Exception as e:
        db.rollback()
        print ("Error: ",e)
    cur.close()
    db.close()

        
       
        
        
        
        

    
    
    
    
        
            
    
    
    
