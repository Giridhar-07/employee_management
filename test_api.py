import requests

r = requests.get('http://127.0.0.1:5000/api/stats')
print('status', r.status_code)
print('headers', r.headers.get('content-type'))
print('text:\n', r.text)
