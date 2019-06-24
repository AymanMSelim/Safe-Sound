# Importing the required moduels
import settings , pygame , sys
import helper_functions as hf
from datetime import datetime
from time import sleep
from threading import Thread

# Reading car dataset 
hf.readLogFile("debug_log.csv")

#start ECU Simulatiom and system timers
hf.runTimers()

# Setup the GUI display
pygame.init()
settings.displayObj = pygame.display.set_mode(settings.Resolution)
pygame.display.set_caption("SafeAndSound")
clock = pygame.time.Clock()

# Program Loop
while(True):
    # log car data into system database every 1.5 second
    if(settings.logFlag and settings.log_timer >= 1.5):
        settings.log_timer = 0
        thread = Thread(target = hf.logSystem)
        thread.start()
    # start a new trip if the car is moving
    if(settings.speed > 0 and not settings.movingFlag):
        settings.movingFlag = True
        x = datetime.today()
        Date = str(x.day)+"-"+str(x.month)+"-"+str(x.year)
        StartTime = str(x.hour)+":"+str(x.minute)+":"+str(x.second)
        thread = Thread(target = hf.startNewTrip , args = (StartTime,Date,))
        thread.start()
    # start trip sum
    hf.tripCalculations()
    # check if there are new dtcs are found
    hf.new_DTCs()
    # run alarm system
    hf.highCoolantTemAlarm()
    hf.apnormalOilTempAlarm()
    hf.intakeSensorFailureAlarm()
    hf.fuelEconomyAlarm()
    if(settings.rpm > 700 and settings.tripFlag):
        hf.MAfSensorFailureAlarm()
    # set the required events
    for event in pygame.event.get():
        # when turn off the Ssstem
        if event.type == pygame.QUIT :   
            settings.stopSystemTimer = True
            hf.setTripDetails()
            pygame.quit()
            sys.exit()
        # when click the touchscreen
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x,y = event.pos
            if (settings.Diagnostic_ass) :
                settings.Diagnostic_ass = False
            elif (settings.Alarm_sys):
                settings.Alarm_sys = False
            elif (settings.normal_state and (x in range(81)) and (y in range(205,286))):
                hf.set_screenNo("inc")
            elif (settings.normal_state and (x in range(715,796)) and (y in range(205,286))):
                hf.set_screenNo("dec")
            elif (settings.normal_state and (settings.screenNo == 0) and (x in range(280,590)) and (y in range(387,508))):
                settings.normal_state = False
                settings.check_state = True
            elif (settings.check_state and (x in range(660,752)) and (y in range(370,404))):
                settings.check_state = False
                settings.normal_state = True
            elif (settings.check_state and (x in range(660,752)) and (y in range(430,464))):
                hf.set_dtcTabNo()
            elif (settings.normal_state) :
                settings.showNo = not settings.showNo
   
    
    # When an alarm is generated
    if(settings.Alarm_sys):
        settings.displayObj.fill(settings.black)
        hf.display_image(settings.alert,-50,0)
        if(settings.alarmNo == 1):
            hf.display_text("MAF Sensor Failure" , 180,-25 , "extra")
        elif(settings.alarmNo == 2):
            hf.display_text("O2 Sensor Failure" , 180,-25 , "extra")
        elif(settings.alarmNo == 3):
            hf.display_text("Intake Sensor Failure" , 180,-25 , "extra")
        elif(settings.alarmNo == 4):
            hf.display_text("High Coolant Temp" , 180,-25 , "extra")
        elif(settings.alarmNo == 5):
            hf.display_text("Apnormal Oil Temp" , 180,-25 , "extra")                                                                                                                                                        
        elif(settings.alarmNo == 6):
            hf.display_text("Low Fuel Economy" , 180,-25 , "extra")

    # When new DTCs are found
    elif(settings.Diagnostic_ass):
        settings.displayObj.fill(settings.white)
        hf.display_image(settings.diagnostic , 55 , -0)
        pygame.draw.rect(settings.displayObj,settings.black,(5,150,790,320),2)
        hf.display_text("New DTCs are found !!",0,-60,"extra")
        i = 0
        for code , desc in settings.newDtcs:
            hf.display_DTC(code + ": " , 10 , 220+30*i , "code")
            hf.display_DTC(desc , 100 , 222+30*i , "desc")
            i += 1

    # when the system at normal state
    elif(settings.normal_state):
        index1 = hf.getTach1()
        index2 = hf.getTach2()
        settings.displayObj.fill(settings.black)
        hf.display_image(settings.logo,280,387)
        hf.display_image(settings.nxtArrow,5,205)
        hf.display_image(settings.prvArrow,715,205)
        if(settings.screenNo == 0):
            hf.display_image(settings.tach_images[index1],320,40)
            hf.display_image(settings.tach_images[index2],85, 40)
            pygame.draw.rect(settings.displayObj,settings.white,(10,10,150,100),2)
            pygame.draw.rect(settings.displayObj,settings.white,(640,10,150,100),2)
            pygame.draw.rect(settings.displayObj,settings.white,(640,370,150,100),2)
            pygame.draw.rect(settings.displayObj,settings.white,(10,370,150,100),2)
            hf.display_image(settings.title,200,5)
            if(not settings.showNo):
                hf.display_text("FuelRate",-315,-160,"property")
                hf.display_text(str(settings.fuelRate)+" L/H",-315,-197,"value")
                hf.display_text("Speed",-115,50,"property")
                hf.display_text(str(settings.speed),-118,0,"value")
                hf.display_text("Throttle",315,-160,"property")
                hf.display_text(str(settings.throttlePosition)+" %",315,-197,"value")
                hf.display_text("RPM",120,50,"property")
                hf.display_text(str(settings.rpm),120,0,"value")
                hf.display_text("Coolant",315,200,"property")
                hf.display_text(str(settings.coolantTemp)+" C",315,161,"value")
                hf.display_text("Intake",-315,200,"property")
                hf.display_text(str(settings.intakeTemp)+" C",-315,161,"value")
            else:
                hf.display_text("RunTime",-315,-160,"property")
                hf.display_text(str(settings.runTime)+" Min",-315,-197,"value")
                hf.display_text("Distance",315,-160,"property")
                hf.display_text(str(settings.distance)+" KM",315,-197,"value")
                hf.display_text("Speed",-115,50,"property")
                hf.display_text(str(settings.speed),-118,0,"value")
                hf.display_text("RPM",120,50,"property")
                hf.display_text(str(settings.rpm),120,0,"value")
                hf.display_text("OilTem",320,200,"property")
                hf.display_text(str(settings.oilTemp)+" C",320,161,"value")
                hf.display_text("Load",-315,200,"property")
                hf.display_text(str(settings.engineLoad)+" %",-315,161,"value")
                

    # check mode
    elif(settings.check_state):
        settings.displayObj.fill(settings.black)
        hf.display_image(settings.title,200,0)
        pygame.draw.rect(settings.displayObj,settings.white,(5,305,620,170),2)
        pygame.draw.rect(settings.displayObj,settings.white,(625,305,168,170),2)
        pygame.draw.rect(settings.displayObj,settings.white,(5,80,788,227),2)
        hf.display_text("Alarms",-93,90,"property")
        hf.display_text("Control",310,90,"property")
        if(len(settings.dtc) > 0):
            hf.display_text("DTCs("+str(settings.dtcTabNo)+")",0,-138,"property")
            start = settings.dtcTabNo * 6
            end = start + 6
            i = 0
            for code , desc in settings.dtc[start:end]:
                hf.display_DTC(code + ":" , 10 , (120 + i*30) , "code")
                hf.display_DTC(desc , 103 , (122 + i*30) , "desc")
                i += 1
        else:
             hf.display_text("DTCs",0,-138,"property")
             hf.display_text("No DTCs are found",0,-35,"value")
             
        hf.display_text("MAF Sensor Failure",-255,130,"alarmOff")
        hf.display_text("O2 Sensor Failure",-263,210,"alarmOff")
        hf.display_text("Intake Sensor Failure",-240,170,"alarmOff")
        hf.display_text("High Coolant Temp",80,130,"alarmOff")
        hf.display_text("Low Fuel Economy",80,210,"alarmOff")
        hf.display_text("Apnormal Oil Temp",80,170,"alarmOff")
        settings.displayObj.blit(settings.clrButton,(660,370))
        settings.displayObj.blit(settings.rtnButton,(660,430))
        if(settings.mafAlarm):
            hf.display_text("MAF Sensor Failure",-255,130,"alarmOn")
        if(settings.o2Alarm):
            hf.display_text("O2 Sensor Failure",-263,210,"alarmOn")
        if(settings.intakeAlarm):
            hf.display_text("Intake Sensor Failure",-240,170,"alarmOn")
        if(settings.coolantAlarm):
            hf.display_text("High Coolant Temp",80,130,"alarmOn")
        if(settings.fuelAlarm):
            hf.display_text("Low Fuel Economy",80,210,"alarmOn")
        if(settings.oilAlarm):
            hf.display_text("Apnormal Oil Temp",80,170,"alarmOn")
	

    # update the dispay
    pygame.display.update()
        

    

	
