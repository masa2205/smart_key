#!/usr/bin/python3
# coding: utf-8

#slackbotを起動するファイル

from slackbot.bot import Bot

def main():
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()
