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

IRC server is ran on `localhost`, port `6667`. Configure your IRC client to access that address.

Set username to `<yourname>/<authprovider>`, e.g. `gitcenter/zeroid.bit`.

## Examples

First, run `python start_server.py`.

### Configuring ThunderBird

1. Open ThunderBird and press `Chat`  
![Chat](images/thunderbird/1.png)
2. Press `Show Accounts`  
![Show Accounts](images/thunderbird/2.png)
3. Press `New Account`  
![New Account](images/thunderbird/3.png)
4. Choose **IRC**  
![IRC](images/thunderbird/4.png)  
5. Use username `<yourname>/<authprovider>` and server `localhost`  
![Login](images/thunderbird/5.png)
6. Leave password empty  
![Password](images/thunderbird/6.png)
7. Open **IRC Options**:
    * Choose port `6667`
    * Uncheck **Use SSL**
    * Press `Next >`  
![IRC Options](images/thunderbird/7.png)
8. Press `Next ->` and then `Finish`  
![Finish](images/thunderbird/8.png)
9. *(optional)* Join channel `lobby`  
![Lobby](images/thunderbird/9.png)

### Configuring mIRC

1. Start mIRC  
![Start mIRC](images/mirc/1.png)
2. Open **mIRC Options**  
![mIRC Options](images/mirc/2.png)
3. Choose `Servers` in sidebar  
![Servers](images/mirc/3.png)
4. Press `Add`  
![Add](images/mirc/4.png)
5. Choose address `localhost` and press `Add`  
![Server](images/mirc/5.png)
6. Press `Select`  
![Select](images/mirc/6.png)
7. Enter nickname `<yourname>/<authprovider>` and press `Connect`  
![Login](images/mirc/7.png)
8. Click `ThunderWave <yourname>/<authprovider>` in sidebar  
![Logging in](images/mirc/8.png)
9. *(optional)* Type `/join #lobby`  
![Joining lobby](images/mirc/9.png)