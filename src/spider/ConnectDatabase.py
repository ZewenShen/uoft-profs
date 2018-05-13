import pymysql

def get_database(path):
    f = open(path, 'r')
    params = f.readlines()
    f.close()
    params = [item.strip('\n') for item in params]
    params[3] = int(params[3])
    return pymysql.connect(host = params[0], user = params[1], password = params[2], port = params[3])
