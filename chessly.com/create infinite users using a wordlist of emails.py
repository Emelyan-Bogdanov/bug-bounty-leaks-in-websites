import asyncio
import aiohttp

url = "https://cag.chessly.com/beta/signup"

# emails to create accounts with
emails = """
james.smith
mary.johnson
john.williams
patricia.brown
robert.jones
jennifer.miller
michael.davis
linda.garcia
william.rodriguez
elizabeth.martin
david.lee
barbara.perez
richard.thomas
susan.taylor
joseph.moore
maria.jackson
thomas.white
james.harris
charlotte.martin
daniel.thompson
sophia.garcia
matthew.martinez
olivia.rodriguez
christopher.lee
amelia.harris
andrew.clark
mia.lewis
joshua.walker
isabella.young
brandon.king
emily.wright
ryan.lopez
madison.scott
jose.hernandez
daniel.green
samantha.adams
anthony.baker
alexander.gonzalez
victoria.morris
jason.nelson
elizabeth.carter
brian.mitchell
karen.perez
kevin.roberts
sophia.lee
michael.hill
emily.martin
james.moore
lisa.white
blake.carter
ella.young
david.green
natalie.morgan
michael.clark
amanda.adams
william.baker
madeline.williams
joseph.jenkins
lucas.martinez
charlotte.harris
michael.thomas
harper.jones
ethan.evans
amelia.thompson
jackson.morris
scarlett.brown
mason.washington
lily.martin
oliver.lee
chloe.harris
elijah.clark
sophia.gonzalez
jack.ramirez
mia.parker
lucas.rodriguez
amelia.sanchez
jackson.hill
harper.moore
michael.taylor
lily.campbell
ethan.morris
ella.williams
mason.jones
scarlett.martin
oliver.brown
chloe.anderson
elijah.wilson
sophia.thomas
jackson.taylor
mia.white
lucas.green
amelia.harris
jack.ramirez
harper.lewis
michael.hernandez
lily.garcia
ethan.martin
ella.martinez
mason.rodriguez
scarlett.williams
oliver.jones
chloe.brown
elijah.taylor
sophia.jackson
jackson.miller
mia.williams
lucas.wilson
amelia.anderson
jack.ramirez
harper.carter
michael.young
lily.harris
ethan.thomas
ella.white
mason.jenkins
scarlett.morris
oliver.wright
chloe.taylor
elijah.anderson
sophia.martin
jackson.harris
mia.jones
lucas.brown
amelia.williams
jack.ramirez
harper.wilson
michael.green
lily.moore
ethan.anderson
ella.taylor
mason.williams
scarlett.jones
oliver.martin
chloe.wright
elijah.williams
sophia.brown
jackson.taylor
mia.martin
lucas.lee
amelia.green
jack.ramirez
harper.anderson
michael.williams
lily.johnson
ethan.williams
ella.jones
mason.martin
scarlett.williams
oliver.johnson
chloe.martin
elijah.kim
sophia.gonzalez
jackson.lee
mia.taylor
lucas.martinez
amelia.rodriguez
jack.ramirez
harper.martin
michael.taylor
lily.wilson
ethan.jones
ella.sanchez
mason.johnson
scarlett.brown
oliver.williams
chloe.anderson
elijah.wilson
sophia.martin
""".replace(".", "").split("\n")


async def create_account(session, email, psw="JT1215060000"):
    headers = {
        "Host": "cag.chessly.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://chessly.com/",
        "Content-Type": "application/json",
        "Origin": "https://chessly.com",
        "Connection": "keep-alive",
        "Cookie": "_ga=GA1.1.674526039.1775739200; _ga_PNQ0H99BWZ=GS2.1.s1775739200$o1$g1$t1775744776$j40$l0$h0; __Secure-cst=1CYyAscIQpOraReOULOX3s_KFiIxCvHH2CY2x6DGccVG",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site"
    }

    body = {
        "email": f"{email}@gmail.com",
        "password": psw
    }

    try:
        async with session.post(url, headers=headers, json=body) as response:
            text = await response.text()
            status = response.status
            print(status)
            if status == 204:
                return f"\nusername : {email}  | password : {psw}"
            if "error" in text:
                print(f"ERROR : {email} ==> {text}")
    except Exception as e:
        print(f"Exception for {email}: {e}")
    return ""


async def create_accounts_concurrently(emails, psw="JT1215060000"):
    async with aiohttp.ClientSession() as session:
        tasks = [create_account(session, email, psw) for email in emails]
        results = await asyncio.gather(*tasks)
    return "\n".join([res for res in results if res])


# Run the async function
log = asyncio.run(create_accounts_concurrently(emails))
with open("users from chessly.com.txt", "w") as file:
    file.write(log)