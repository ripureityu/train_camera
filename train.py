import requests

url ="http://localhost:3000/"
paramas = {"key1":"value1","key2":"value2"}
responce = requests.get(url, params=paramas)
print(responce.status_code)
print(responce.text)
