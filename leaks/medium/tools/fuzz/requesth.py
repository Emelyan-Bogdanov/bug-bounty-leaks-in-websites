import os
import requests
from colors import *


def get(url, wordlist,successed=0):
    try:
        r = requests.get(url)
        if r.status_code not in [403 , 404]:
            successed += 1
            print(f"[{successed} found][{r.status_code}] {green(url)}")
        else:
            print(f"[{successed} found][{r.status_code}] {yellow(url)}")
            
            if os.path.exists(f"results/{wordlist}/{r.status_code}.txt"):
                with open(f"results/{wordlist}/{r.status_code}.txt", "a+") as file:
                    file.write(str(url.replace("https://medium.com/", "")) + "\n")
            else :
                print(f"created : ", f"results/{wordlist}/{r.status_code}.txt")
                with open(f"results/{wordlist}/{r.status_code}.txt", "w") as file:
                    file.write(str(url.replace("https://medium.com/", "")) + "\n")
        return r.status_code
    except Exception as e:
        print(red(f"ERROR : {url} : {str(e)}"))
        return 999  # error
