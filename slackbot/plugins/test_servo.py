import pigpio

SERVO_PIN = 23

    pi = pigpio.pi()
    pi.set_servo_pulsewidth(SERVO_PIN, 2500)

#set_servo_pulsewidthの値を500~2500の範囲で駆動指定し最小値、最大値を把握
#最小値、最大値が割り出せたら中央値を割り出す
#今回使用したモーターは500~2500駆動、中央値は1500だったが鍵を実装させる際にモーターに取り付けた部品の都合上、初期値は1850に設定