# *アレクサとラズベリーパイを使用し、声で家の鍵を開けれるようにした*  
  <br>
<img width="300" alt="travel" src="https://user-images.githubusercontent.com/65245621/111405210-6f844580-8713-11eb-8565-d95b77bdbc84.PNG">

　<br>
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
    * Python  
    * Slackbot  

- 3.使用した外部サービス  
    * Slack  
    * IFTTT  
  <br>

***
  <br>

- ラズパイセットアップ  

  ・Raspbian(OS)のダウンロード  
    1. ラズパイに直接キーボード、モニターを接続    <font color="green"># USBキーボード、HDMIケーブル、HDMIで接続できるモニターを使用</font>
    2. ラズパイを起動  
    3. CHOOSE OS をクリックして利用するイメージを選択  
    4. CHOOSE SD CARD をクリックして書き込み先のSDカードを選択  
    5. WRITEボタンをクリックして書き込み  
    6. Raspbian(OS)をインストール  

  ・初期設定   <font color="green">#「Welcome to Raspberry Pi」のウィンドウに従って、初期設定を進める  </font>
    1. 地域選択  
    2. デフォルトユーザのパスワードを入力  
    3. wi-fi設定  

  ・IPアドレスの固定   # 無線LANの場合  
   ```
    $ sudo vim /etc/dhcpcd.conf   # 設定ファイルを開く

      interface wlan0  #末尾に追加  
      static ip_address=[設定したい固定IPアドレス]/24  
      static routers=[デフォルトゲートウェイのIPアドレス]  
      static domain_name_servers=[DNSサーバーのIPアドレス]  
   ```   
   ラズパイを再起動し、反映されているか確認    

  ・SSH,VNCの設定  
    1. 空ファイルの作成
    ```
     $ sudo touch /boot/ssh  
    ```
    2. 設定からSSHを有効にする  
    3. 設定からパスワードを変更   <font color="green"># デフォルト ユーザー名:'pi', パスワード:raspberry</font>  
    4. ラズパイを再起動  
    5. 別のPCからSSHで接続確認  
    ```
     $ ssh ラズパイのユーザー名@ラズパイのIPアドレス  
    ```    
    6. パスワード入力  

  ・Python3.7.0のインストール  
   ```
    $ python3 -V   # バージョンの確認  
    $ sudo apt update   # コンパイルに必要になるライブラリをインストール  
    $ sudo apt upgrade  
    $ sudo apt install libffi-dev libssl-dev openssl  
    $ wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz    # ソースコードのダウンロード  
    $ tar zxvf Python-3.7.2.tgz    # コンパイル  
    $ cd Python-3.7.2  
    $ ./configure  
    $ make  
    $ sudo make install  
    $ python3 -V    # バージョンの確認  
    $ sudo pip3 install --upgrade pip    # pipのアップデート  
    $ pip3 --version  
    ```
  <br>

    ***
  <br>

- slack上での作業  
  
  ・slack上でチャンネル、botの作成  
  ・APIトークンの取得  
  <br>

  ***
  <br>

- Pythonのslackbotライブラリでslackbotを作る  

  ・slacbotライブラリのインストール 
  ``` 
     $ sudo pip3 install slackbot  
  ```   

  ・slacbotを起動させるファイル構成  
  ```
  slackbot                   # プログラムをまとめるディレクトリ  
   ├─ run.py                 # botを起動させるプログラム  
   ├─ slackbot_settings.py   # botの設定を行うファイル  
   └─ plugins                # botの機能を格納したディレクトリ  
      ├─ __init__.py     # プラグインとして認識してもらうための空ファイル  
      └─ exec.py         # 機能をコーディングするファイル 
   ```       
     ターミナル上にて以下のコマンドで構成  
     ```
   $ mkdir slackbot  
   $ cd slackbot  
   $ touch run.py slackbot_settings.py  
   $ mkdir plugins  
   $ cd plugins  
   $ touch __init__.py exec.py  
     ```       

  ・slackbotの初期設定  
     run.py  slackbot_settings.py exac.pyファイルの中身をコーディング   
      <font color="green"># この時点ではbotの機能のみの実装  </font>

  ・slackbotを起動し動作確認  
  ```
     $ python3 run.py  
  ```   

  ・botのデーモン化   <font color="green"># run.pyファイルをデーモン化する </font>

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
  <br>

     ***
  <br>

- サーボモーターの制御   # サーボモーターの動作確認  


  ・pigpioライブラリのインストール  
  ```
        $ sudo apt install pigpio
        $ sudo pigpiod   # 起動  
        $ sudo systemctl enable pigpiod.service   # 自動起動  
        $ sudo shutdown -r now  #　確認作業  
        $ sudo systemctl status pigpiod.service  
  ```      

  ・ラズパイの制御信号の指定と接続  
  
  ・サーボモータの駆動範囲を調べる  
  ```
        $ python3 test_servo.py パルス幅  
  ```      

  ・exec.pyファイルに組み込む  

  ・slack上で特定の文字を入力し、サーボモーターの駆動とメンションリプライの返信を確認する  
  <br>

  ***
  <br>

- slackとAlexaの連携  

  ・IFTTTを使用しIFTTT上で設定   <font color="green"># スマホでもPCでも同じ操作 </font> 
    1. IFTTTのメニューからCreateを選択  
    2. Thisをクリック  
    3. Choose serviceからAlexaを検索  
    4. connectをクリック  
    5. Say a Specific Phrase トリガーを選択  
    6. What phrase?　欄にトリガーとなる文字を入力し、Create triggerボタンをクリック  
    7. Thatをクリック  
    8. Choose serviceからslackを検索  
    9. Post to channelをクリック  
    10. チャンネル名を選択  
    11. Messageを追加  
    12. Create actionをクリック  
    13. continueをクリック  
    14. Finishをクリック  


  ・Alexa上で特定の言葉を設定し、音声認識によりIFTTTの発動条件と連携させる     
         <font color="green">#スマホのアレクサアプリから設定  </font>
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
  <br>

    ***
  <br>

- サーボモーターを実装し、鍵に取り付ける  
