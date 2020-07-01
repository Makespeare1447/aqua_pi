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
ambient_pin = 20
led_fan_pin = 27
buzzer_pin = 22


lamp = io.LED(pin=lamp_pin, active_high=False)
ambient_led = ip.LED(pin=ambient_pin, active_high=False)

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
lighttime_interval = (9,19)  #time interval for lights on
ambient_interval = (19,22)
main_delay = 2             #delay in seconds for main loop
#chat_id = set your telegram chat id here (or from configuration file)

#absolute maximum values:
# placeholder

#set device states (setup)
lamp.off()
ambient_led.off()

led_fan.off()

beep(buzzer)      #initial startup beep

start_time = round(set_starttime(), 1)

print('starting up...\n')
bot.send_message(chat_id=chat_id, text='Hello Sir, i am starting up now...\n')
hours = gethours()
minutes = getminutes()
oldhours = hours
oldminutes = minutes
##########################################################   MAIN LOOP  #################################################################################

while(True):

    #get actual time:
    hours = gethours()
    minutes = getminutes()
    timestamp = gettimestamp()


    #check if lighttime:
    if(hours>=lighttime_interval[0] and hours<lighttime_interval[1]):
        lighttime = True
    else:
        lighttime = False

    #check if ambient_time:
    if(hours>=ambient_interval[0] and hours<ambient_interval[1]):
        ambient_time = True
    else:
        ambient_time = False


    #light control:
    if(lighttime==True):
        lamp.on()
        lampstate = True
    else:
        lamp.off()
        lampstate = False

    
    #ambient control:
    if(ambient_time==True):
        ambient_led.on()
    else:
        ambient_led.off()


    #printing out information
    print('Water Temperature: {}'.format(water_temp) + ' deg')
    print('Led Temperature: {}'.format(led_temp) + ' deg')
    print('Cycles: {}'.format(cycles))
    print('Seconds since program start: {}'.format(int(round(time_since_start(start_time), 0))))
    if lampstate==True:
        print('light is on\n')
    else:
        print('light is off\n')

    # report by telegram:
    if minutes!=oldminutes:
        try:
            bot.send_message(chat_id=chat_id, text='Up and running!\nlampstate = {}\nruntime: {} seconds'.format(lampstate, int(round(time_since_start(start_time), 0))))
        except:
            print('telegram message was not sent successful - maybe network connection dropped out!')
    
    oldhours = hours
    oldminutes = minutes
    cycles = cycles + 1   
    sleep(main_delay)  #main delay


