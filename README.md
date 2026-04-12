# bug-bounty-leaks-in-websites



in this repository , i put all bugs i found in all websites


-------------------
## 1. free api for chatbot model : found trick
- website : `https://talkai.info/chat/`
- trick : use zaproxy to intercept the send message request and replace the token_front with a rtandom string (because the system doesn't check its validity)
- code : [talkAi.py](https://github.com/Ibrahimibrahimi/bug-bounty-leaks-in-websites/blob/main/talkAiAPI.py)
## 2. another **free api model** found by intercepting requests
- website : `https://api.deepai.org/`
- trick : use zaproxy to intercept the send message request and replace the token_front with a rtandom string (because the system doesn't check its validity)
- code : [deepAiApi.py](https://github.com/Ibrahimibrahimi/bug-bounty-leaks-in-websites/blob/main/deepAiApi.py)
## 3. Sensitive directories at **chari.com**
- the website is made by phpmyadmin
- leaks & access public for folders like chari.com/mysql ... 
- results : [leaks.txt](https://github.com/Ibrahimibrahimi/bug-bounty-leaks-in-websites/blob/main/chari.com-results.txt)
## 4. IDOR in request at **lichess.org**
- probability to be an _IDOR_ (im not 100% sure)
- Results : [results lichess](https://github.com/Ibrahimibrahimi/bug-bounty-leaks-in-websites/blob/main/lichess%20foundations.txt)
  ### Task :
    1. Analyse the hex hash in the middle
    2. the hash origin is a _base64_ encrypted
    3. result = base64(username|unkown hash|email)
## 5. Unsecured files found at [esta official website](ecours.esta.ac.ma)
- the website is based on *moodle* wich is open source
- check the files inside [.gitignore](https://github.com/moodle/moodle/blob/main/.gitignore) and test them in website directory
- use some fuff tools to save found directories
## 6. Can Create infinite emails using wordlist , found at [chessly](chessly.com) 
  - the plateform doesn't verify the emails or send a code verification
  - use the python file inside `/targets/chessly/create.... .py`
## 7. free xp_farmer unlimited (xp_farmer.py)[https://github.com/Ibrahimibrahimi/bug-bounty-leaks-in-websites/blob/main/chessly.com/xp_farmer.py]
  - you use the interval (2.5) to not get banned
  - you extract the cookies from your account , and you replace it in the accoun
  - you can read the same variation more than 5 times
  - wait like 3-7 minutes , so the system generate new uuid for the lessons (`if you keep without waiting , you're litterally wasting your time , because you'll see somthing like Response Body: {"points":0,"challengePoints":0} , that means no points added`)


## 8. _Secure-cst cookie in (chessly)[chessly.com]
  - the cst is a `SWR React Query Cache Key`or maybe `Opaque token`
