import json
import requests

response = requests.post('http://localhost:6000/generate', 
              data={'user-id': '1', 'generation-date': '2023-05-04 00:00:00', 'user-goal': 'lose', 'user-level': 'intermidiate'})

print(response.json())