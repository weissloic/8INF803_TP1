import sys
from bs4 import BeautifulSoup
import requests
import re
from Spell import *
from personnage import *


def check_upper_name(string):
    last_char = string[-1]
    if last_char.isupper():
        string = string[:-1]
        return check_upper_name(string)
    return string

def main(args):
    #try:
    page = requests.get("https://aonprd.com/Spells.aspx?Class=All")
    HTML_PARSER='html.parser'
    soup = BeautifulSoup(page.content, HTML_PARSER)

    for url in soup.find_all('td'):
        spellListHtmlPage = BeautifulSoup(str(url), HTML_PARSER)
        spellDisplayDiv = spellListHtmlPage.find('a')
        spellName = spellDisplayDiv.get("href").split("=")[1]
        spell_class = Spell(spellName)

        spellPage = requests.get("https://aonprd.com/SpellDisplay.aspx?ItemName=" + spell_class.url)
        soup = BeautifulSoup(spellPage.content, HTML_PARSER)
        spellDiv = soup.find(id="ctl00_MainContent_DataListTypes_ctl00_LabelName")

        #classStringWithlevel = re.search(r"Level<\/b>(.*?)<h", str(spellDiv))
        spell_class.components = re.search(r"Components<\/b>(.*?)<h", str(spellDiv)).group(1).split(",")

        print("---------------------------------\n")

        print(spellName)
        print("url : " + spell_class.url)
        print("components : ")
        print(spell_class.components)

        #if classStringWithlevel:
        #   print(classStringWithlevel.group(1))
        #else:
        #   print(spellDiv)

    #except:
    #    print("error")
    #    sys.exit(84)

if __name__ == "__main__":
    sys.exit(main(sys.argv))