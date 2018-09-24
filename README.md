## QuestBot
Telegram Bot powered by django and allowing to construct complex quests.
There are following features:
1) Ability to define conditions depends on different action types (Button Click, Command, Callback, Message)
2) Current/Default chat keyboard
3) Events based on asynchronous calls to send response to a particular chat
4) Steps with only one initial and handlers attached to them
5) Responses with replay keyboard, message and feature-rich settings


## How to
1) Install [docker](https://docs.docker.com/engine/installation/) and 
[docker-compose](https://docs.docker.com/compose/install/)
2) Clone this repository ```git clone https://github.com/pm-str/QuestBot```
3) Run ```docker-compose up``` (admin credentials ``root/rootroot``)

After that you should create telegram bot and [obtain api token](https://core.telegram.org/bots#botfather)

4) Last step is to set up url of your site (__Sites__ section in django admin)

As well in development mode it can be used either [localtunnel](https://github.com/localtunnel/localtunnel)
or [ngrok](https://github.com/inconshreveable/ngrok) in testing purposes. 
However, they have a limit on requests number and don't ensure stable connection too.


