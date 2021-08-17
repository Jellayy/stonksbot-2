from configparser import ConfigParser

config = ConfigParser()

config['General'] = {
    'Command Prefix': 'gib',
    'Monitored Stocks': 'GME,AMC,AAL,ACB,AG,AMD,BB,BBBY,BYDDY,BYND,CCIV,CLOV,CRIS,CTRM,EXPR,EZGO,GM,GTE,HIMS,INO,JAGX,KOSS,MRNA,NAKD,NCTY,NOK,NVAX,OPEN,RKT,RLX,RYCEY,SBUX,SHLS,SIEB,SLV,SNDL,SOXL,TIRX,TR,TRVG,WKHS,XM,ZOM',
    'Statusbar Stocks': 'GME,AMC',
    'Alert Channel': 'investing',
    'Alert Role ID': '848759692120948736',
}

config['Misc'] = {
    'Status Update Timer (Seconds)': '10',
}

config['Developer Settings'] = {
    'Debug Channel': 'debug',
}

with open('../config.ini', 'w') as f:
    config.write(f)
