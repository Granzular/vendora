import os,socket

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
ip = '127.0.0.1'
port = 8000
try:
    s.connect(('8.8.8.8',80))
    ip = s.getsockname()[0]

except:
    print('couldnt connect, defaulting to 127.0.0.1')
    pass

cmd = f'python manage.py runserver {ip}:{port} --settings=mysite.settings.development'
print(ip)


os.system(cmd)


