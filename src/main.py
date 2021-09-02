import sys
from bs4 import BeautifulSoup
import requests


def check_upper_name(string):
    last_char = string[-1]
    if last_char.isupper():
        string = string[:-1]
        return check_upper_name(string)
    return string


class Potion:
    def __init__(self, name):
        self.name = name
        self.url = name.replace(" ", "%20").replace("'", "%27")

def main(args):
    try:
        page = requests.get("https://aonprd.com/Spells.aspx?Class=All")
        soup = BeautifulSoup(page.content, 'html.parser')

        for url in soup.find_all('td'):
            tmp = url.text.replace("\n", "")
            if tmp[0] == " ":
                tmp = tmp.replace(" ", "", 1)
            tmp = tmp.split(":")
            tmp = tmp[0]
            tmp = check_upper_name(tmp)
            #print(tmp)

            tmp_class = Potion(tmp)

            print(tmp_class.url)

    except:
        print("error")
        sys.exit(84)

if __name__ == "__main__":
    sys.exit(main(sys.argv))