rabbitracer
===========


# これは何？

RabbitMQ に流れる全てのメッセージを JSON でダンプするためのスクリプトです。
RabbitMQ も用いたシステムのデバッグに有用です。

# インストール

インストールと実行には Python が必要です。

```
$ git clone https://github.com/momijiame/rabbitracer.git
$ cd rabbitracer
$ python setup.py install
```

# 使い方

RabbitMQ が起動した状態で Firehose 機能を有効にします。

```
$ rabbitmqctl stop_app
$ rabbitmqctl trace_on
$ rabbitmqctl start_app
```

スクリプトを実行すると RabbitMQ に流れるメッセージが JSON で出力されます。
デフォルトではローカルホストにゲストアカウントで接続します。
変更する場合はオプションで指定できます。

```
$ rabbitracer
```
