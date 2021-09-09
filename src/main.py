import sys
from bs4 import BeautifulSoup
import requests
import re
from potion import *
from personnage import *


def check_upper_name(string):
    last_char = string[-1]
    if last_char.isupper():
        string = string[:-1]
        return check_upper_name(string)
    return string

def main(args):
    #try:
    counter = 0
    page = requests.get("https://aonprd.com/Spells.aspx?Class=All")
    soup = BeautifulSoup(page.content, 'html.parser')

    for url in soup.find_all('td'):
        print(counter)
        test = BeautifulSoup(str(url), 'html.parser')
        tag = test.find('a')
        tmp = tag.get("href").split("=")
        tmp = tmp[1]
        tmp_class = Potion(tmp)

        print(tmp_class.name)

        print(tmp_class.url)

        page = requests.get("https://aonprd.com/SpellDisplay.aspx?ItemName=" + tmp_class.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        div = soup.find(id="ctl00_MainContent_DataListTypes_ctl00_LabelName")

        #if tmp_class.name == "Agonize":
        #    print(div)


        print("---------------------------------\n")
        #print(div)
        x = re.search(r"Level<\/b>(.*?)<h", str(div))
        #print("ui")
        #result = re.match(pattern, test_string)

        if x:
            print(x.group(1))
        else:
            print(div)

        counter += 1

    #for test in soup.find_all('tbody'):
            #test = BeautifulSoup(str(test), 'html.parser')
           # print(soup.prettify())
            #print(tag)
            #x = re.search("^<b>Level.*[\n].*[\n]<$", str(test))
            #print(test)



        #print(page.content)

    #except:
    #    print("error")
    #    sys.exit(84)

if __name__ == "__main__":
    sys.exit(main(sys.argv))