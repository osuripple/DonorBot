## DonorBot

- Origin: https://git.zxq.co/ripple/DonorBot
- Mirror: https://github.com/osuripple/DonorBot

This Discord bot handles custom roles (and custom username colors) for Ripple donors.

## Requirements
- Python 3.5
- MySQLdb (`mysqlclient`)
- Discord.py
- Bottle
- Gevent

## Setting up
Install the dependencies
```
$ pip install -r requirements.txt
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