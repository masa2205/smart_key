from slackbot.bot import listen_to      # チャンネル内発言で反応するデコーダ

import pigpio
import time

@listen_to('open')
def open_key(message):

    SERVO_PIN = 23 #ラズパイのピンを指定

    pi = pigpio.pi()
    pi.set_servo_pulsewidth(SERVO_PIN, 2500)
    time.sleep(2.5)

    pi.set_servo_pulsewidth(SERVO_PIN, 1850)

    message.reply('opened！')

@listen_to('close')
def close_key(message):

    SERVO_PIN = 23

    pi = pigpio.pi()
    pi.set_servo_pulsewidth(SERVO_PIN, 1200)
    time.sleep(2.5)

    pi.set_servo_pulsewidth(SERVO_PIN, 1850)

    message.reply('closed！') 