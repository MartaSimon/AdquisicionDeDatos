import requests

url = "https://api.twitter.com/1.1/users/show.json?screen_name=martasp_2"

API_KEY_Twitter = "xaSzPjwGshWJTqLXADYUPUHnS"
ACCESS_TOKEN_Twitter = "2698508264-YgWteCidNLT8ljU22Ew2P6xFLxYTNIQR0bdNqrE"
oauth_signature = "jFP3dkTcdjxrdQM9HHDu4eBlo8g%3D"
oauth_nonce = "X7uF5abw4ch"

payload={}
headers = {
  'Authorization': f'OAuth oauth_consumer_key="{API_KEY_Twitter}",oauth_token="{ACCESS_TOKEN_Twitter}",oauth_signature_method="HMAC-SHA1",oauth_timestamp="1672746906",oauth_nonce="{oauth_nonce}",oauth_version="1.0",oauth_signature="{oauth_signature}"',
  'Cookie': 'guest_id=v1%3A166741246587632259'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)