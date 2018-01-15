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

1. ![Chat](images/thunderbird/1.png)  
    Open ThunderBird and press `Chat`  
2. ![Show Accounts](images/thunderbird/2.png)  
    Press `Show Accounts`  
3. ![New Account](images/thunderbird/3.png)  
    Press `New Account`  
4. ![IRC](images/thunderbird/4.png)  
    Choose **IRC**  
5. ![Login](images/thunderbird/5.png)  
    Use username `<yourname>/<authprovider>` and server `localhost`  
6. ![Password](images/thunderbird/6.png)  
    Leave password empty  
7. ![IRC Options](images/thunderbird/7.png)  
    Open **IRC Options**:  
    * Choose port `6667`
    * Uncheck **Use SSL**
    * Press `Next >`  
8. ![Finish](images/thunderbird/8.png)  
    Press `Next ->` and then `Finish`  
9. ![Lobby](images/thunderbird/9.png)  
    *(optional)* Join channel `lobby`.  