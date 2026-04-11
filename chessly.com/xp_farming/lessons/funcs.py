
import requests

# extract cookie


def getCookie():
    COOKIE = "_ga=GA1.1.984846494.1775748892; _ga_PNQ0H99BWZ=GS2.1.s1775748891$o1$g1$t1775757980$j36$l0$h0;"
    email = "eldoradogpt2025@gmail.com"  # email of test account
    password = "JT1215060000"  # password of the test account
    url = "https://cag.chessly.com/beta/login"
    headers = {
        "Host": "cag.chessly.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://chessly.com/",
        "Content-Type": "application/json",
        "Origin": "https://chessly.com",
        "Connection": "keep-alive",
        "Cookie": COOKIE,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site"
    }
    payload = {
        "email": email,
        "password": password
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        cst_cookie = response.cookies.get('__Secure-cst')
        COOKIE += f"__Secure-cst={cst_cookie}"
        return COOKIE
    except requests.RequestException as e:
        print("Cant get cookie =========>",e)
        exit()

###########################################


def getCourses(cookie, category="openings"):
    url = f"https://cag.chessly.com/beta/{category}/courses"
    headers = {
        "Host": "cag.chessly.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://chessly.com/",
        "Origin": "https://chessly.com",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses
    data = response.json()

    # Extract all "id" values from the response
    ids = [item["id"] for item in data if "id" in item]
    return ids

#######################################



def readOpLesson(uuid):
    url = f"https://cag.chessly.com/beta/progress/openings/studies/variations/{uuid}"
    headers = {
        "Host": "cag.chessly.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://chessly.com/",
        "Origin": "https://chessly.com",
        "Connection": "keep-alive",
        "Cookie": getCookie(),
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Content-Length": "0"
    }

    try :
        response = requests.post(url, headers=headers)
        data = response.json()
        print(data)
        return True
    except :
        return False
    
def getVariations(cookie,uuid,category="openings"):
    url = f"https: // cag.chessly.com/beta/{category}/courses/{uuid}/chapters"
    headers = {
        "Host": "cag.chessly.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://chessly.com/",
        "Origin": "https://chessly.com",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Content-Length": "0"
    }

    try :
        response = requests.get(url, headers=headers)
        print(response.status_code)
        print(response.text)
        data = response.json()
        ids = [item["id"] for item in data if "id" in item]
        return ids
    except :
        print("cant get variations !!")
    
