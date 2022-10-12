import requests

endpoint = "https://api.assemblyai.com/v2/transcript"

json = {
  "audio_url": "https://storage.googleapis.com/bucket/b2c31290d9d8.wav"
}

headers = {
  "Authorization": "<your auth key>",
  "Content-Type": "application/json"
}

response = requests.post(endpoint, json=json, headers=headers)
print(response.json())
