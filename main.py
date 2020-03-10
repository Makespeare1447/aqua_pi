#####################################################################################################################################################
########################                                    HEADER                              #####################################################
#####################################################################################################################################################


print('setting parameters and importing libraries...')

########################################################### IMPORTS #################################################################################
from functions_and_modules import *

##########################################################   SETUP  #################################################################################
#setup is executed once at startup
#setting permissions (necessary for sending image)
print('setting permissions...')
os.system('sudo chmod -R 777 .')

#pin declaration:
#lamp and pump are connected to the double relais module
#fan1: humidity regulation, fan2: inhouse ventilation (air movement)
lamp_pin = 17
filter_pin = 27
fan1_pin = 21
fan2_pin = 20
dht1_pin = 4
buzzer_pin = 22


lamp = io.LED(pin=lamp_pin, active_high=False)
filter = io.LED(pin=filter_pin, active_high=False)
buzzer = io.TonalBuzzer(buzzer_pin)
fan1 = io.PWMLED(fan1_pin)
fan2 = io.PWMLED(fan2_pin)
bot = telegram.Bot(token=token) #token comes from your configuration.py file


#variable initialisation:
errorcounter = 0
temperature = 0
hours = 0
hours_old = 0
minutes = 0
minutes_old = 0
cycles = 0                 #cyclenumber for debugging
wateringcycles = 0
emergencystate = False
lampstate = False
humidity_list = []
temperature_list = []
timestamp_list = []
seconds_since_start_list = []
co2_list = []
tvoc_list = []

#parameter declaration:
watering_active = False
maxerrors = 5
daytime_interval = (10,18)  #time interval for lights on
pumptime = 8              #seconds for plantwatering per wateringcycle
main_delay = 1             #delay in seconds for main loop
#chat_id = set your telegram chat id here (or from configuration file)

#absolute maximum values:


#set device states (setup)
lamp.off()
filter.off()
fan1.off()

beep(buzzer)      #initial startup beep

start_time = round(set_starttime(), 1)

print('starting up...\n')
bot.send_message(chat_id=chat_id, text='Hello Sir, i am starting up now...\n')

print('venting air on startup...')
bot.send_message(chat_id=chat_id, text='venting air on startup...\n')
fan1.on()
fan2.on()
sleep(15)
fan1.off()
fan2.off()

hours = gethours()
minutes = getminutes()
oldhours = hours
oldminutes = minutes
##########################################################   MAIN LOOP  #################################################################################

while(True):
    try:
        #get actual time:
        hours = gethours()
        minutes = getminutes()
        timestamp = gettimestamp()

        #shutdown in the evening :
        if(hours==21):
            print('good night! - shutting down...')
            bot.send_message(chat_id, text='good night! - shutting down...')
            os.system("sudo shutdown now")


        #reboot in the morning :
        if((hours==9 and hours!=oldhours)):
            print('good morning! - rebooting...')
            bot.send_message(chat_id, text='good morning! - rebooting...')
            os.system("sudo shutdown -r now")


        #check if daytime:
        if(hours>=daytime_interval[0] and hours<daytime_interval[1]):
            daytime = True
        else:
            daytime = False


        #light control:
        if(daytime==True and emergencystate==False and humidity>humidity_min and humidity<85 and temperature<=temp_max 
        and temperature>=temp_min):
            lamp.on()
            lampstate = True
        else:
            lamp.off()
            lampstate = False

            


            

        #printing out information
        print('Temperature: {}'.format(temperature) + ' deg')
        print('Cycles: {}'.format(cycles))
        print('Seconds since program start: {}'.format(int(round(time_since_start(start_time), 0))))
        if lampstate==True:
            print('light is on\n')
        else:
            print('light is off\n')


        oldhours = hours
        oldminutes = minutes
        cycles = cycles + 1   
        sleep(main_delay)  #main delay


    except:
        errorcounter = errorcounter + 1
        print('Error occured! - errorcounter = {}'.format(errorcounter))
        bot.send_message(chat_id, text='Error occured! - errorcounter = {}'.format(errorcounter))
        if errorcounter>=maxerrors:
            print('5 errors occured - terminating program now...')
            bot.send_message(chat_id, text='{} errors occured - terminating program...'.format(maxerrors))
            raise ValueError('A very specific bad thing happened')
