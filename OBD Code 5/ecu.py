# Importing required modules
from threading import Thread
import obd , settings

# global variable represents connection between Python-OBD and ECU
connection = None 

class obdThread(Thread):
# Constructor function that creats and starts obd thread
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
        
# Function that contains what thread will do 
    def run(self):
        global connection
        # For depugging purposes(shows everything will happend during connection)
        obd.logger.setLevel(obd.logging.DEBUG)
        # Scan for available ports
        ports = obd.scan_serial()
        if(len(ports) > 0 ):
            #creat connection object with specified properties
            connection = obd.Async(portstr = ports[0] , fast = False)
        else:
           print("There is no available serial ports")
           return 0
        
        # The car parameters that wanted to be monitored
        connection.watch(obd.commands.RPM, callback = self.new_rpm)
        connection.watch(obd.commands.SPEED, callback = self.new_speed)
        connection.watch(obd.commands.INTAKE_TEMP, callback = self.new_intake_temp)
        connection.watch(obd.commands.COOLANT_TEMP, callback = self.new_coolant_temp)
        connection.watch(obd.commands.OIL_TEMP, callback = self.new_oil_temp)
        connection.watch(obd.commands.AMBIANT_AIR_TEMP, callback = self.new_ambiant_temp)
        #connection.watch(obd.commands.DISTANCE_SINCE_DTC_CLEAR, callback = self.new_distance)
        connection.watch(obd.commands.ENGINE_LOAD, callback = self.new_engine_load)
        connection.watch(obd.commands.FUEL_RATE, callback = self.new_fuel_rate)
        connection.watch(obd.commands.THROTTLE_POS, callback = self.new_throttle_position)
        connection.watch(obd.commands.MAF, callback = self.new_MAF)
        connection.watch(obd.commands.RUN_TIME, callback = self.new_run_time)
        #connection.watch(obd.commands.MONITOR_O2_B1S1, callback = self.new_o2Sen_test)
        # The car problems or issues if there are
        connection.watch(obd.commands.GET_DTC, callback=self.new_dtc)
        # Start the Asynchronous connection(threaded updated loop to keep track the subscriped car parameters)
        connection.start()
        # setting this flag to boot GUI
        settings.ecuReady = True


    # functions that recievs the responses and set global variables
    def new_o2Sen_test(self,r):
        tests = r.value
        maxVoltT = tests.MAX_VOLTAGE
        minVoltT = tests.MIN_VOLTAGE
        settings.o2MaxVolt = maxVoltT.value
        settings.o2MinVolt = minVoltT.value
    
    def new_rpm(self, r):
        settings.rpm = int(round(r.value.magnitude))
		
    def new_speed(self, r):
        settings.speed = int(round(settings.speed.magnitude))
			
    def new_intake_temp(self, r):
        settings.intakeTemp = int(round(r.value.magnitude))
		
    def new_MAF(self, r):
        settings.MAF = round(r.value.magnitude,2)
		
    def new_throttle_position(self, r):
        settings.throttlePosition = int(round(r.value.magnitude))
		
    def new_dtc(self, r):
        settings.dtc = r.value

    def new_ambiant_temp(self, r):
        settings.ambiantTemp = int(round(r.value.magnitude))

    def new_fuel_rate(self, r):
        settings.fuelRate = round(r.value.magnitude,2)

    def new_oil_temp(self,r):
        settings.oilTemp = int(round(r.value.magnitude))

    def new_engine_load(self,r):
        settings.engineLoad = int(round(r.value.magnitude))

    def new_run_time(self,r):
        print(r.value.magnitude)
        settings.runTime = round(r.value.magnitude/60,2) 

    def new_distance(self,r):
        settings.distance = round(r.value.magnitude - settings.refDistance , 2)

    
	

        
        
        
