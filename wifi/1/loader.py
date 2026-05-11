import json


with open("./1/1.har", "r") as file:
    data = json.load(file)

for log in data["entries"]:
    
    # request
    request = log["request"]
    method = request["method"]
    url = request["url"]
    cookies = request["cookies"]  # list of {"name":"kk","value":"kk"}

    postData = request["postData"]
    postText = postData["text"]

    # response
    response = log["response"]
    