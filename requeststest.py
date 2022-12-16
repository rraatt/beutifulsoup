import requests

payload = {'username': 'rraatt', 'password': 'testing'}
r = requests.post('https://httpbin.org/post', data=payload)

print(r.json())
