########################################################### IMPORTS ###############################################################################
import matplotlib
matplotlib.use('Agg')
import time
from time import sleep
import os
import sys
import matplotlib.pyplot as plt
#import pandas as pd
import numpy as np
import gpiozero as io
from gpiozero.tones import Tone 
from smbus2 import SMBusWrapper, i2c_msg               #for i2c devices
#import Adafruit_DHT
#import Adafruit_Python_SSD1306   #oled if necessary
import telegram
from configuration import *




########################################################### FUNCTIONS ###############################################################################

def gettimestamp():
        timestamp = time.strftime("%H:%M:%S")
        return timestamp


def gethours():
    hours = time.strftime("%H")
    return int(hours)


def getminutes():
    minutes = time.strftime("%M")
    return int(minutes)

    
def beep(buzzer):
    buzzer.play(Tone(500.0)) # Hz
    sleep(0.15)
    buzzer.stop()
    sleep(0.15)
    buzzer.play(Tone(500.0)) # Hz
    sleep(0.15)
    buzzer.stop()


def set_starttime():
        start_time = time.time()
        return start_time

def time_since_start(start_time):
        return((time.time() - start_time))


def report_per_telegram(bot, chat_id, temperature, humidity, co2, tvoc, cycles, wateringcycles, lampstate):
        if lampstate==True:
                bot.send_message(chat_id=chat_id, text='Humdity: {0} %\nTemperature: {1} deg\nCo2: {2} ppm\nTVOC: {3} ppb\nCycles: {4}\nWateringcycles: {5}\nlamp on '.format(humidity, temperature,
                co2, tvoc, cycles, wateringcycles))
        else:
                bot.send_message(chat_id=chat_id, text='Humdity: {0} %\nTemperature: {1} deg\nCo2: {2} ppm\nTVOC: {3} ppb\nCycles: {4}\nWateringcycles: {5}\nlamp off '.format(humidity, temperature,
                co2, tvoc, cycles, wateringcycles))
                


def send_plot_per_telegram(bot, chat_id):
        print('sending plot per telegram...')
        bot.send_message(chat_id=chat_id, text='sending plot per telegram...')
        sleep(3)
        bot.send_photo(chat_id=chat_id, photo=open('\home\Veggie_Pi\plot.png', mode='rb'))
        sleep(3)