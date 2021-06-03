from configparser import ConfigParser

config = ConfigParser()

config['General'] = {
    'Command Prefix': 'gib',
    'Monitored Stocks': 'GME,AMC',
    'Daily Summary Stocks': 'GME,AMC',
    'Alert Channel': '***',
    'Alert Role ID': '***',
}

config['Misc'] = {
    'Status Update Timer (Seconds)': '30',
}

with open('../config.ini', 'w') as f:
    config.write(f)
