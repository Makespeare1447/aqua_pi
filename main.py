#####################################################################################################################################################
########################                                    HEADER                              #####################################################
#####################################################################################################################################################


print('setting parameters and importing libraries...')

########################################################### IMPORTS #################################################################################
from functions_and_modules import *

##########################################################   SETUP  #################################################################################
#setup is executed once at startup
#setting permissions (necessary for sending image)
#print('setting permissions...')
#os.system('sudo chmod -R 777 .')

#pin declaration:
#lamp and pump are connected to the double relais module

lamp_pin = 21
filter_pin = 20
led_fan_pin = 27
buzzer_pin = 22


lamp = io.LED(pin=lamp_pin, active_high=False)
filter = io.LED(pin=filter_pin, active_high=False)
buzzer = io.TonalBuzzer(buzzer_pin)
led_fan = io.PWMLED(led_fan_pin)

bot = telegram.Bot(token=token) #token comes from your configuration.py file


#variable initialisation:
errorcounter = 0
water_temp = 0
led_temp = 0
hours = 0
hours_old = 0
minutes = 0
minutes_old = 0
cycles = 0                 #cyclenumber for debugging
emergencystate = False
lampstate = False
timestamp_list = []
seconds_since_start_list = []


#parameter declaration:
maxerrors = 5
lighttime_interval = (10,18)  #time interval for lights on
main_delay = 1             #delay in seconds for main loop
#chat_id = set your telegram chat id here (or from configuration file)

#absolute maximum values:
# placeholder

#set device states (setup)
lamp.off()
filter.off()
led_fan.off()

beep(buzzer)      #initial startup beep

start_time = round(set_starttime(), 1)

print('starting up...\n')
#bot.send_message(chat_id=chat_id, text='Hello Sir, i am starting up now...\n')
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


        #check if lighttime:
        if(hours>=lighttime_interval[0] and hours<lighttime_interval[1]):
            lighttime = True
        else:
            lighttime = False


        #light control:
        if(lighttime==True):
            lamp.on()
            lampstate = True
        else:
            lamp.off()
            lampstate = False


        #printing out information
        print('Water Temperature: {}'.format(water_temp) + ' deg')
        print('Led Temperature: {}'.format(led_temp) + ' deg')
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
            bot.send_message(chat_id, text='{} errors occured - terminating program...'.format(maxerrors))
            raise ValueError('{} errors occured - program terminated.')
