# ThunderProxy

ThunderProxy is a local IRC server connecting [ThunderWave](https://github.com/AnthyG/ThunderWave) and [ThunderBird](https://www.thunderbird.net/) (or any other IRC client).

## TODO

1. Send messages to group chats
2. Receive messages from group chats
3. Send messages to private chats
4. Receive messages from private chats
5. ~~Send messages via IRC to lobby~~
6. ~~Receive messages from lobby~~

## Installation and usage

Linux:

```bash
$ git clone https://github.com/imachug/ThunderProxy.git
$ cd ThunderProxy
$ vi config.py
$ sudo python start_server.py # Run local IRC server
```

Windows:

```
> git clone https://github.com/imachug/ThunderProxy.git
> cd ThunderProxy
> notepad config.py
> python start_server.py # Run local IRC server
```

## Local server

IRC server is ran on `localhost`, port `6697`. Configure your IRC client to access that address.