import requests
from requests import Request, Session
import json

b_url = "http://10.10.1.2:8069"
# or "http://201.100.100.12:8069" (or whatever the ip is)
url = "{}/web/session/authenticate".format(b_url)

db = "TokyoHotel"
user = "admin"
passwd = "admin_odoo"

s = Session()

data = {
    'jsonrpc': '2.0',
    'params': {
        'context': {},
        'db': db,
        'login': user,
        'password': passwd,
    },
}

json_data = json.dumps(data)

headers = {
    'Content-type': 'application/json'
}

req = Request('POST', url, data=json_data, headers=headers)

prepped = req.prepare()

resp = s.send(prepped)
print(resp.text)

session_id = json.loads(resp.text)['result']['session_id']
print(session_id)
date = {'check_in': '2018-04-29 07:00:00', 'check_out': '2018-05-01 05:00:00'}
get_room_availabilities = '/get_room_availabilities/' + str(date)

res = requests.get(b_url + get_room_availabilities, cookies={'session_id': str(session_id)})
print(res.text)

