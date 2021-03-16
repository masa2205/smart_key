#botに対するトリガー、リプライの指定と、サーボモーターの制御

from slackbot.bot import listen_to  #チャンネル内発信で反応するデコーダー

import pigpio  #ラズパイのGPIOを制御するためのライブラリ
import time

@listen_to('open')  #チャンネル内へのメッセージ
def open_key(message):  #鍵を開ける際のサーボモーターの制御

    SERVO_PIN = 23  #ラズパイの制御信号の指定

    pi = pigpio.pi()  ##GPIOにアクセスするためのインスタンス
    pi.set_servo_pulsewidth(SERVO_PIN, 2500)  #サーボモーターを90度回す
    time.sleep(2.5)

    pi.set_servo_pulsewidth(SERVO_PIN, 1850)  #サーボモーターを初期値に戻す

    message.reply('opened！')  #botからのメンションリプライ

@listen_to('close')  
def close_key(message):  #鍵を閉める際のサーボモーターの制御

    SERVO_PIN = 23

    pi = pigpio.pi()
    pi.set_servo_pulsewidth(SERVO_PIN, 1200)  #サーボモーターを90度開ける方向と反対に回す
    time.sleep(2.5)

    pi.set_servo_pulsewidth(SERVO_PIN, 1850)

    message.reply('closed！')