## DonorBot

## Requirements
- Python 3.5
- MySQLdb (`mysqlclient` or `mysql-python`)
- Discord.py
- Bottle
- Gevent

## Setting up
Install the dependencies
```
$ pip install discord.py mysqlclient bottle gevent
```
Then run the bot once to create the config file
```
$ python3 donorbot.py
```
Edit the config file with your ripple db credentials and discord bot/server info
```
$ nano config.json
```
...and run the bot
```
$ python3 donorbot.py
```

## License
All code in this repository is licensed under the GNU AGPL 3 License.  
See the "LICENSE" file for more information  
This project contains code taken by reference from [miniircd](https://github.com/jrosdahl/miniircd) by Joel Rosdahl.
