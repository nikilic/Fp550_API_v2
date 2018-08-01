import requests
import json
#response = requests.post('http://httpbin.org/post', data={'key1':'value1'})
#response = requests.get('http://httpbin.org/post')
#response = requests.get('http://0.0.0.0:8090/g11_cmd')
#url='http://0.0.0.0:8090/greeting/dusan'
#url='http://0.0.0.0:8090/g11_cmd'

url='https://fp550api.localtunnel.me/g11_cmd'
response = requests.get(url)

"""
print(response.request.body)
print(response.request.headers.keys)
print("aaa")
print (response.headers)
print (response.content)
print (response.status_code)
"""
resp_dict=json.loads(response.text)
print (resp_dict)

data_str=""
for m in resp_dict['recv_pck_Data']:
    data_str=data_str + chr(m)
print ("\n Fiscal Printer Current  Date and Time: ",data_str)
