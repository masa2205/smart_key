from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャンネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ


@listen_to('あけて')
def listen_func(message):
    message.send('おはよう！')

@respond_to('あけて')
def mention_func(message):
    message.reply('あけたよ！') # メンション    