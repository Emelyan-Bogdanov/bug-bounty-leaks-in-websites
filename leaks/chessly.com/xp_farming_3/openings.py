import requests , time
from cookies import get_secure_cst_cookie


def getLessonVariations(course_uuid):
    # example : carocan : d4f3504b-8bbd-4435-ae30-a0b8372c9286
    url = f"https://cag.chessly.com/beta/openings/courses/{course_uuid}/chapters"
    headers = {
        "Host": "cag.chessly.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://chessly.com/",
        "Origin": "https://chessly.com",
        "Connection": "keep-alive",
        "Cookie": get_secure_cst_cookie(),
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    time.sleep(1)
    b = [lesson["id"] for lesson in response.json()]
    print("Found" , len(b)," Variations")
    return b
############ to read

import requests

def readLessonVariation(uuid):
    url = f"https://cag.chessly.com/beta/progress/openings/studies/variations/{uuid}"
    headers = {
        "Host": "cag.chessly.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://chessly.com/",
        "Origin": "https://chessly.com",
        "Connection": "keep-alive",
        "Cookie": get_secure_cst_cookie(),
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site"
    }

    response = requests.post(url, headers=headers)
    print("CODE : ",response.status_code)
    time.sleep(1)
    if response.status_code == 200 : 
        points = response.json()["points"]
        print("Got ",points," points")
        if points > 0 :
            print("Points : ",points)
            print("Repeating reading the lesson")
            readLessonVariation(uuid)
        else :
            return points
    return  0# how much points