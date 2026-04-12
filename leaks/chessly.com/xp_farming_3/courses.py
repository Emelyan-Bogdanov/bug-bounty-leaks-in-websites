import requests , time
from cookies import get_secure_cst_cookie


def extractAllLessonsUUID(category: str = "openings"):
    url = f"https://cag.chessly.com/beta/{category}/courses"

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
        "Sec-Fetch-Site": "same-site",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse JSON response
        data = response.json()
        # Extract all UUIDs from the 'id' fields
        uuids = [item['id'] for item in data if 'id' in item]

    return uuids


def xp_from_lesson_part_uuid(uuid):
    url = f"https://cag.chessly.com/beta/progress/openings/studies/variations/{uuid}/drills/completion"
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
        "Sec-Fetch-Site": "same-site",
    }
    response = requests.post(url, headers=headers)
    print(f"UUID: {uuid} - Status Code: {response.status_code}")
    print("Response Body:", response.text)
    # if 5 points => re read the same lesson
    # points
    print(response.text)
    points = response.json().get("points",0)
    if points > 0:
        print(f"Points > {points} ==> read again")
        time.sleep(2)
        xp_from_lesson_part_uuid(uuid)
    else:
        print("enough points ==> next lesson part")
