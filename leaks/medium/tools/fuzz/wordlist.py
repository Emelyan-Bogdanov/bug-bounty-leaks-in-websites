import os


WS_PATH = "../wordlists/"

# load wordlists
def getWordlists():
    # create path of all wordlists
    ws = os.listdir(WS_PATH)
    for w in ws :
        try :
            os.mkdir(f"results/{w}")
        except :
            print("",end="")
    return ws


def load(wordlist:str):
    with open(f"{WS_PATH}/{wordlist}","r",encoding="utf-8") as file :
        return [i.strip() for i in file.readlines()]
