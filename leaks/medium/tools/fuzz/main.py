import os
from requesth import *
from colors import *
from wordlist import getWordlists, load

found = []
successed = 0

# load wordlists + content
print(yellow("loading wordlists..."))
RESULT = {}


def saveResult(r):
    import json
    with open('RESULT.json', 'w') as js:
        json.dump(r, js)
    print("SAVED JSON")


# start
URL = "https://medium.com/"
wordlists = getWordlists()
for wordlist in wordlists:
    print(red(f"===========[{wordlist}]=============="))
    words = load(wordlist)
    for word in words:
        # build the url
        url = f"{URL}{word}"

        # try
        code = get(url, wordlist, successed)

        # save to json
        if code in RESULT:
            RESULT[code].append(url)
        else:
            RESULT[code] = [url]

        if successed % 5 == 0 :
            saveResult(RESULT)

        if code != 999:
            # not found
            found.append(word)
            if code not in [403,404] :
                successed += 1

            # save to file
            with open("result.txt", "w") as file:
                for f in found:
                    file.write(f + "\n")
