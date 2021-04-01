import requests
import json

url = "http://91.109.25.86:8888/api/Rebuild/base64"

f = open("base64.sample", "r")
base64_value = f.read()

payload = json.dumps({
  "Base64": base64_value
})

headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
