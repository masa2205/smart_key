# *AlexaとRaspberry Piを使用し、声で家の鍵を開けれるようにした*  

<img width="300" alt="完成品" src="https://user-images.githubusercontent.com/65245621/111405210-6f844580-8713-11eb-8565-d95b77bdbc84.PNG">

***

# IoT概要

### スマートロック(Alexa,slack連携)

<br />

- 新型コロナウィルスの流行による非接触方IoTの推奨が進められている昨今、鍵ノブに触れずに鍵の開閉ができるスマートロック(ドアノブは手動になってしまいます。ご容赦下さい。)  

- slackbotへ特定のメッセージを送ることにより、鍵の開閉が可能。

- Alexaによる音声認識機能による、鍵の開閉が可能。

- 遠隔での鍵の開閉が可能。

<br />

開発から制作まで全て独学で開発致しました。

<br />
<br />

***

# 開発した背景

私自身もともとAlexaを使用したスマートホーム化に興味を持っており、様々な電化製品はAlexaの音声認識スキルによって動かせることができるようにしています。  
自宅のスマートロック化に勤しんでいる中、株式会社Quriosさんのスマートロックが世に台頭し、スマートロックの認知が進みました。私も購入を考えましたが、当時の税込価格で約¥33,000と即決できるような価格ではありませんでした。  
そんな中、小学生が夏休みの自由研究で、音声で動かせるロボットを自作したというニュースをたまたま拝見し、「もしかしたらスマートロックも自分で作れるのでは」と思い立ち、どうせ作るならプログラミングの学習をしながら且つ、Quriosさんが販売してる値段よりも下回らないと時間と労力が勿体無いので、予算も決めつつ、Quriosさんがどのような収益構造を作っているのか(仮に同じ材料、部品を使っていると仮定し、市販の値段がこのくらいであれば業者と直接やりとりし大量発注するならばこのくらいの値段か、等)を想像しながらビジネスモデルに対する知見も深めれて、一石五鳥くらいの経験ができるではないかと考えたのがきっかけです。  
また私自身現在ルームシェアをしており、1人1本鍵を持てておりません(特殊な鍵で複製が不可なため)。スマートロックを取り付けることにより、鍵を持たずとも誰でも開閉ができるようになるので、誰が何時に帰ってくるから今日は誰々が鍵を持っていって、等の面倒臭いやり取りが解消されるとも考えたためです。  

<br />
<br />

***

# 工夫した点

- 機能を細分化しそれぞれのissueに落とし込み、都度テストを繰り返し正常な動作、バグを洗い出しながらの丁寧なGit flowを意識した開発

- Gitチーム開発を意識したissue・プルリクエストの活用

- 完成までのスピード感を意識し、必要最低限の機能と可読性を重視したコードを意識

- 自分が詰まった点や、解決に時間がかかった点等を共有し、私のような初学者でも読めば完成まで辿り着けるようなReadmeの作成(自身のアウトプットにも活用)

<br />
<br />

***
# 追加機能予定

- 権限追加

- NFCリーダーで交通系電子マネーでの開閉機能

<br />
<br />

***
# 用意したもの、使用技術

- 1.用意した物  
    * Raspberry Pi(以下ラズパイ) 3 model B+  

    * MacBook pro  

    * Amazon Alexa  

    * サーボモーター(20kg.cm)  

    * 電池式モバイルバッテリー  

    * SDカード  

    * USBマイクロA  

    * HDMIケーブル  

    * USBキーボード  

    * スリーエムテープ  

    * ドライバー等工具  

- 2.使用したプログラム  

    * Python  3.7.3

    * Slackbot  

- 3.使用した外部サービス  

    * Slack  

    * IFTTT  

    * Alexa home skill
  
<br />
<br />

***
# 実際の制作手順

## 1. ラズパイセットアップ  

<br />

- Raspbian(OS)のダウンロード  

1. ラズパイに直接キーボード、モニターを接続(USBキーボード、HDMIケーブル、HDMIで接続できるモニターを使用)

2. ラズパイを起動  

3. CHOOSE OS をクリックして利用するイメージを選択  

4. CHOOSE SD CARD をクリックして書き込み先のSDカードを選択  

5. WRITEボタンをクリックして書き込み  

6. Raspbian(OS)をインストール  

<br />

- 初期設定(「Welcome to Raspberry Pi」のウィンドウに従って、初期設定を進める)  

1. 地域選択  

2. デフォルトユーザのパスワードを入力  
3. wi-fi設定  

<br />

- IPアドレスの固定(無線LANの場合)
```
   $ sudo vim /etc/dhcpcd.conf  (設定ファイルを開く)

   interface wlan0  #末尾に追加  
   static ip_address=[設定したい固定IPアドレス]/24  
   static routers=[デフォルトゲートウェイのIPアドレス]  
   static domain_name_servers=[DNSサーバーのIPアドレス]  
```   
ラズパイを再起動し、反映されているか確認    

<br />

- SSH,VNCの設定  

1. 空ファイルの作成
```  
   $ sudo touch /boot/ssh  
```
2. 設定からSSHを有効にする  

3. 設定からパスワードを変更(デフォルト ユーザー名:'pi', パスワード:raspberry)

4. ラズパイを再起動  

5. 別のPCからSSHで接続確認  
```    
   $ ssh ラズパイのユーザー名@ラズパイのIPアドレス  
```
6. パスワード入力  

***
<br />

## 2.Python3.7.0のインストール  

<br />

```
   $ python3 -V (バージョンの確認)  
   $ sudo apt update (コンパイルに必要になるライブラリをインストール)  
   $ sudo apt upgrade  
   $ sudo apt install libffi-dev libssl-dev openssl  
   $ wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz ースコ  ードのダウンロード)
   $ tar zxvf Python-3.7.2.tgz (コンパイル)  
   $ cd Python-3.7.2  
   $ ./configure  
   $ make  
   $ sudo make install  
   $ python3 -V  (バージョンの確認)  
   $ sudo pip3 install --upgrade pip (pipのアップデート)  
   $ pip3 --version  
```

***

<br />

## 3.slack上での作業  

<br />
  
1. slack上でチャンネル、botの作成  

2. APIトークンの取得  

***

<br />

## 4.Pythonのslackbotライブラリでslackbotを作る  

<br />


1. slacbotライブラリのインストール 
``` 
   $ sudo pip3 install slackbot  
```   

2. slacbotを起動させるファイル構成  
```
   slackbot                    # プログラムをまとめるディレクトリ  
     ├─ run.py                 # botを起動させるプログラム  
     ├─ slackbot_settings.py   # botの設定を行うファイル  
     └─ plugins                # botの機能を格納したディレクトリ  
         ├─ __init__.py        # プラグインとして認識してもらうための空ファイル  
         └─ exec.py            # 機能をコーディングするファイル 
```       

3. ターミナル上にて以下のコマンドで構成  
```
   $ mkdir slackbot  
   $ cd slackbot  
   $ touch run.py slackbot_settings.py  
   $ mkdir plugins  
   $ cd plugins  
   $ touch __init__.py exec.py  
 ```       

4. slackbotの初期設定  
```
   run.py  slackbot_settings.py exac.pyファイルの中身をコーディング  (この時点ではbotの機能のみの実装)
```
5. slackbotを起動し動作確認  
```
   $ python3 run.py  
```   
***

<br />

## 5.botのデーモン化(run.pyファイルをデーモン化する)

<br />

1. /etc/systemd/system/以下にserviceファイルを作成  
```
   $ sudo vim /etc/systemd/system/run_daemon.service 
```    
2. run.pyファイルの先頭にPythonの宣言コードを追加  
```
   #!/usr/local/pyenv/shims/python  
```   
3. rund.serviceファイルの設定  

```
   [Unit]  
   Description = slackbot daemon  

   [Service]  
   Type = simple  
   Restart = on-failure  
   ExecStart = ../../smart_key/slackbot/run.py  # run.pyまでの絶対パス  
   user=macan  

   [Install]  
   WantedBy = multi-user.target  
```   

4. 実行権限を与える  
```
   $ sudo chmod 755 /etc/systemd/system/run_daemon.service  
```   
5. 起動  
```
   $ sudo systemctl start run_daemon    
```   
6. ステータスの確認  
```
   $ sudo systemctl status run_daemon  
```   
7. プログラムをOSの起動時に自動で実行するように設定  
```
   $ sudo systemctl enable run_daemon  
```   
8. 再起動して動作の確認  
```
   $ sudo reboot  
```   
9. 再度ステータスの確認  
```
   $ sudo systemctl status run_daemon  
```   
10. デーモン化の停止   # コードの編集をまだ行うため  
```
   $ sudo systemctl stop run_daemon  
```   

***

<br />

## 6.サーボモーターの制御(サーボモーターの動作確認)  

<br />

1. pigpioライブラリのインストール  
```
   $ sudo apt install pigpio
   $ sudo pigpiod (起動)  
   $ sudo systemctl enable pigpiod.service (自動起動)
   $ sudo shutdown -r now  (確認作業)  
   $ sudo systemctl status pigpiod.service  
```      

2. ラズパイの制御信号の指定と接続  
  
3. サーボモータの駆動範囲を調べる  
```
   $ python3 test_servo.py パルス幅  
```      

4. exec.pyファイルに組み込む  

5. slack上で特定の文字を入力し、サーボモーターの駆動とメンションリプライの返信を確認する  

***

<br />

## 7.slackとAlexaの連携  

<br />

### ・IFTTTを使用しIFTTT上で設定(スマホでもPCでも同じ操作)

<br />

1. IFTTTのメニューからCreateを選択  

2. Thisをクリック  

3. Choose serviceからAlexaを検索  

4. connectをクリック  

5. Say a Specific Phrase トリガーを選択  

6. What phrase?　欄にトリガーとなる文字を入力し、Create triggerボタンリック 

7. Thatをクリック  

8. Choose serviceからslackを検索  

9. Post to channelをクリック  

10. チャンネル名を選択  

11. Messageを追加  

12. Create actionをクリック  

13. continueをクリック  

14. Finishをクリック  

<br />

### ・Alexa上で特定の言葉を設定し、音声認識によりIFTTTの発動条件と連携させる(スマホのアレクサアプリから設定)  

<br />

1. その他 をタップ  

2. 定形アクション をタップ  

3. 定形アクション名を入力  

4. 実行条件を設定  

5. 音声をタップ  

6. フレーズを入力  

7. アクションを追加  

8. IFTTTを選択  

9. IFTTT上で作成したアプレットを追加  

10. 次へ をタップし完了  

11. アレクサにフレーズを話しかけて、一連の流れが実行されるか確認  

<br />

***

<br />

## 8.サーボモーターを工作し、鍵に取り付ける  

<br />

*工作に関しましてはモーターを100円ショップで購入できるようなプラスチック等の容器に取り付け、鍵ノブに開閉時の挙動を確認し取り付けるだけです。  
ドアが傷つかないようにQuriosさんも使用しているスリーエムというテープを使用するのがおすすめです。

<br />

***

<br />

## 感想

<br />

初めてのプログラミング、IoTの自作でしたが、テストの時点で自分の思った通りの挙動になった時はとても達成感が生まれ、ITの道へ進もうと決断できた経験でした。  
生活の中の小さなことかもしれませんが、面倒臭いことを効率化できたことによるストレスの軽減や生活の質の向上はIT産業の醍醐味だと思います。  
今後も何か面白そうなIoTがあればまずは自作できないか考えてみたいと思います。  
最後まで読んでいただきありがとうございました。