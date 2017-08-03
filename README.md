このライブラリについて
----

#### 原作: [https://github.com/carpedm20/LINE](https://github.com/carpedm20/LINE)

注意
----
かなり前に書いたものなのであまりいい実装が出来ていません。(動作確認はしましたが)


必要なもの
----

- Python3(Python2でも動くけど動作安定しないかも)
- Pythonのライブラリ
  - requests
  - thrift
  - simplejson

インストール方法
----

gitコマンドを使います。

```git clone https://github.com/in9lude/line.git```

その後、プロジェクトディレクトリに入り、  
```python setup.py install```
とすればインストール完了です。

使い方
----
```python:
from line import LineClient #LineClientをimport
# LineClientオブジェクト(これがAPIラッパーです)
client = LineClient(mail, password) #ログイン
print(client.profile.displayName) #ユーザーネームを表示
```

ログイン方法はいくつかあります。  
__URLでログインする方法__
```python:
from line import LineClient #LineClientをimport
client = LineClient() #URLログイン
AUTH URL: line://au/q/P1aQ1BnZxmKEdXTsFViy43uOa4OAkSsa #このリンクをモバイル端末に踏ませてログイン完了
```

ログインさえできればあとは簡単です。

ここで簡単なbotのコードを紹介します。

```python:
from line import LineClient, PollManager
try:
    client = LineClient(email, password)
    print("{}:LOGIN SUCCESS".format(client.profile.name))
except:
    print("LOGIN FAILED")

poll = PollManager(client)

def sendMessage(text, to, _from, toType=0, contentMetadata=0):

    msg = Message()

    if to[0] == "c":

        msg.to = to
        msg._from = _from
        msg.toType = 2

    elif to[0] == "u":
        msg.to = _from
        msg._from = to

    if contentMetadata:
        msg.contentMetadata = contentMetadata

    msg.text = text

    client.sendMessage(msg)

def RECEIVE_MESSAGE(op):

    msg = op.message
    # print(msg)
    print(
    " TO: {}\n".format(msg.to),
    "FROM: {}\n".format(msg._from),
    "TEXT: {}\n".format(msg.text),
    "CONTENT TYPE: {}\n".format(msg.contentType),
    "METADATA: {}\n".format(msg.contentMetadata),
    "TYPE: {}\n".format(msg.toType),
    "MESSAGE ID: {}\n".format(msg.id),
    "DATE: {}\n\n".format(msg.createdTime)
    )

    if msg.contentType != 0:
        pass

    else:
        text = msg.text
        to = msg.to
        _from = msg._from

        sendMessage(msg.text, to, _from)

poll.addFunction(26, RECEIVE_MESSAGE)

while True:

    poll.start()
```

これは発言したことをそのまま返すエコーbotの例です。

__関数一覧は追記予定です__
