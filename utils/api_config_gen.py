from configparser import ConfigParser

config = ConfigParser()

config['APIs'] = {
    'Discord.py API Key': '***',
    'Polygon API Key': '***',
}

with open('../api.ini', 'w') as f:
    config.write(f)
