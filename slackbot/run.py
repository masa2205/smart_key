#!/usr/bin/python3
# coding: utf-8
from slackbot.bot import Bot
import time

def main():
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    time.sleep(3)
    print('start slackbot')
    main()