import requests
import json
#response = requests.post('http://httpbin.org/post', data={'key1':'value1'})
#response = requests.get('http://httpbin.org/post')
#response = requests.get('http://0.0.0.0:8090/g11_cmd')
#url='http://0.0.0.0:8090/greeting/dusan'
#url='http://0.0.0.0:8090/g11_cmd'

url='https://fp550irvas.localtunnel.me/g12_cmd'
# url='https://fp550irvas.localtunnel.me/g12_cmd'
response = requests.get(url)


print(response.request.body)
print(response.request.headers.keys)
print("aaa")
print(response.json)
print (response.headers)
print (response.content)
print (response.status_code)

resp_dict=json.loads(response.text)
print (type(resp_dict))
# print (len(resp_dict.items()))
if type(resp_dict) is str:
    print(resp_dict)
else:
    data_str = ""

    for m in resp_dict['recv_pck_Data']:
        data_str=data_str + chr(m)

    print ("\n Fiscal Printer Current  Date and Time or 'PIB': ",data_str)

