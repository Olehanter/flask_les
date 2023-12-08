import requests


response = requests.post("http://127.0.0.1:5000/hello/world",
                         json={"name": "user_1", "password": "1234"},
                         headers={'token': 'some_token'},
                         params={'name': 'John', "age": 20}
                         )
# response = requests.get("http://127.0.0.1:5000")


print(response.status_code)
print(response.text)
