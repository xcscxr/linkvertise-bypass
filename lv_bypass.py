import re
import time
import json
import base64
import requests

# -------------------------------------------

def lv_bypass(url):
    client = requests.Session()
    
    headers = {
        "User-Agent": "AppleTV6,2/11.1",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    
    client.headers.update(headers)
    
    url = url.replace("%3D", " ").replace("&o=sharing", "").replace("?o=sharing", "").replace("dynamic?r=", "dynamic/?r=")
    
    id_name = re.search(r"\/\d+\/[^\/]+", url)
    
    if not id_name: return None
    
    paths = [
        "/captcha", 
        "/countdown_impression?trafficOrigin=network", 
        "/todo_impression?mobile=true&trafficOrigin=network"
    ]
    
    for path in paths:
        url = f"https://publisher.linkvertise.com/api/v1/redirect/link{id_name[0]}{path}"
        response = client.get(url).json()
        if response["success"]: break
    
    data = client.get(f"https://publisher.linkvertise.com/api/v1/redirect/link/static{id_name[0]}").json()

    out = {
        'timestamp':int(str(time.time_ns())[0:13]),
        'random':"6548307", 
        'link_id':data["data"]["link"]["id"]
    }
    
    options = {
        'serial': base64.b64encode(json.dumps(out).encode()).decode()
    }
    
    data = client.get("https://publisher.linkvertise.com/api/v1/account").json()
    user_token = data["user_token"] if "user_token" in data.keys() else None
    
    url_submit = f"https://publisher.linkvertise.com/api/v1/redirect/link{id_name[0]}/target?X-Linkvertise-UT={user_token}"
    
    data = client.post(url_submit, json=options).json()
    
    return data["data"]["target"]

# -------------------------------------------

# Add URL
url = "https://domain.tld/XXXXXX/XXX" 
bypassed = lv_bypass(url)

print(bypassed)
