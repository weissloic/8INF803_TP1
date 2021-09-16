import sys
from bs4 import BeautifulSoup
import requests
import re
from Spell import *
from personnage import *

HTML_PARSER = 'html.parser'

class Utils:
    def check_upper_name(self, string):
        last_char = string[-1]
        if last_char.isupper():
            string = string[:-1]
            return Utils.check_upper_name(self, string)

        return string


class Parsing:
    def __init__(self):
        self.counter_error = 0
        self.spell_found = False
        self.counter_spell_not_displayed = 0
        self.baseUrl = "https://aonprd.com/"

    def init_soup(self, url):
        page = requests.get(self.baseUrl + url)
        soup = BeautifulSoup(page.content, HTML_PARSER)

        return soup

    def get_spell_name(self, url):
        spellListHtmlPage = BeautifulSoup(str(url), HTML_PARSER)
        spellDisplayDiv = spellListHtmlPage.find('a')
        spellName = spellDisplayDiv.get("href").split("=")[1]

        return spellName

    def get_nice_parsing(self, find_infos, name):
        if "Spell Resistance" not in find_infos.group(0):
            self.counter_spell_not_displayed += 1
            regex = name + "<\/h1>.*(Level<\/b>(.*?)<.*(Components<\/b>(.*?)<h)()).*Description<\/h3>"
            self.spell_found = False
        else:
            self.spell_found = True
            regex = name + "<\/h1>.*(Level<\/b>(.*?)<.*(Components<\/b>(.*?)<h).*(Spell Resistance<\/b>(.*?)<h).*).*<\/h3>?"

        return regex

    def extract_spell_list( self, spell_string):
        spell_list = {}

        for spell in spell_string.split(","):
            spell_and_level = re.search(r"(.*)\s(.*)",spell[1:])
            spell_list[spell_and_level.group(1)]=spell_and_level.group(2)

        return spell_list


def main(args):
    #try:
        tt = Utils()
        prs = Parsing()

        soup = prs.init_soup("Spells.aspx?Class=All")


        for url in soup.find_all('td'):
            spell_class = Spell(prs.get_spell_name(url))
            soup = prs.init_soup("SpellDisplay.aspx?ItemName=" + spell_class.url)
            spellDiv = soup.find(id="ctl00_MainContent_DataListTypes")


            if "(" in spell_class.name:
                spell_class.name = spell_class.name.replace("(", "\(").replace(")", "\)")


            regex = spell_class.name + "<\/h1>.*(Level<\/b>(.*?))<.*Description<\/h3>"
            spellDiv = str(spellDiv).replace("\n", "")

            find_infos = re.search(regex, str(spellDiv))


            if find_infos:
                regex = prs.get_nice_parsing(find_infos, spell_class.name)
                print("name class: " + spell_class.name)
                find_infos = re.search(regex, str(spellDiv))
                print("classe linked:",prs.extract_spell_list(find_infos.group(2)))
                print("Components: " + find_infos.group(4))

                if prs.spell_found == True:
                    print("Spells Resistance: " + find_infos.group(6))
                else:
                    print("Spells Resistance: " + "no")
            else:
                prs.counter_error += 1

            print("error: ", prs.counter_error)
            print("spell not displayed: ", prs.counter_spell_not_displayed)

            print("---------------------------------\n")
   # except:
    #    print("error")
    #    sys.exit(84)

if __name__ == "__main__":
    sys.exit(main(sys.argv))