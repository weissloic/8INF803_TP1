import sys
from bs4 import BeautifulSoup
import requests
import re
from Spell import *
from pymongo import MongoClient
from random import randint
from bson.code import Code

import sqlite3

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
        self.base_url = "https://aonprd.com/"

    def init_soup(self, url):
        page = requests.get(self.base_url + url)
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

    def extract_spell_list(self, spell_string):
        spell_list = {}

        for spell in spell_string.split(","):
            print(spell)
            if spell[-1] == ' ':
                spell = spell[:-1]
            spell_and_level = re.search(r"(.*)\s(.*)", spell[1:])
            spell_list[spell_and_level.group(1)] = spell_and_level.group(2)

        return spell_list

    def get_minimum_level(self, spell_list):
        minValue = min(spell_list.items(), key=lambda x: x[1])
        key_min = min(spell_list.keys(), key=(lambda k: spell_list[k]))
        return spell_list[key_min]

class MongoDB:

    def __init__(self):
        self.client = MongoClient("mongodb://root:rootpassword@localhost:27017")
        self.db = self.client.business

    def map_reduce_request(self):
        collection = self.db.delete_me

        map = Code("function () {"
                   "  var level_wiz;"
                   "if (this.components.includes(' V') && this.components.length == 1) {"
                   "if (this.class_linked.includes('wizard')) {"
                   " level_wiz = this.class_linked.split('wizard ')[1];"
                   "if (parseInt(level_wiz) < 4)"
                   " emit(this.name, this.components)"
                   "}"
                   "}"
                   "}")

        reduce = Code("function (key, values) {"
                      "  var total = 0;"
                      "}")

        result = collection.map_reduce(map, reduce, "myresults")
        counter = 0

        for doc in result.find():
            counter += 1
            print(doc)

        print(counter)

class mySql():
    def __init__(self):
        self.conn = sqlite3.connect('example.db')


def getComponent(find_infos):
    print("Components: " + find_infos.group(4))

    tmpComponent = find_infos.group(4)
    if tmpComponent.find('('):
        tmpComponent = re.sub(r"\([^()]*\)", "", find_infos.group(4))

    print(tmpComponent.split(","))
    listComp = tmpComponent.split(",")
    listComp = [x.strip(' ') for x in listComp]
    print(listComp)

    return listComp

def getResistance(find_infos, spell_found):
    if spell_found:
        print("Spells Resistance: " + find_infos.group(6))
        if "yes" in find_infos.group(6):
            return True
        else:
            return False
    else:
        return False

def getLevel(classLinked, prs):
    level = 0

    if "wizard" in classLinked:
        level = int(classLinked.split("wizard ")[1])
    else:
        spell_list = prs.extract_spell_list(classLinked)
        level = prs.get_minimum_level(spell_list)

    return level

def getClassLinked(find_infos):

    if find_infos.group(2).find('('):
        tmp = re.sub(r"\([^()]*\)", "", find_infos.group(2))
    else:
        tmp = re.sub(r"\([^()]*\)", "", find_infos.group(2))

    return tmp

def main(args):
    # try:

    tt = Utils()
    prs = Parsing()
    mongo = MongoDB()
    mongo.map_reduce_request()

    """soup = prs.init_soup("Spells.aspx?Class=All")

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
            print(re.sub(r"\([^()]*\)", "", find_infos.group(2)))

            spell_class.classLinked = getClassLinked(find_infos)
            spell_class.level = getLevel(spell_class.classLinked, prs)
            spell_class.components = getComponent(find_infos)
            spell_class.resistance = getResistance(find_infos, prs.spell_found)

            spell = {
                'name': spell_class.name,
                'level': spell_class.level,
                'class_linked': spell_class.classLinked,
                'components': spell_class.components,
                'spell_resistance': spell_class.resistance
            }

            #result = mongo.db.reviews.insert_one(spell)
        else:
            prs.counter_error += 1


        print("error: ", prs.counter_error)
        print("spell not displayed: ", prs.counter_spell_not_displayed)
        print("---------------------------------\n")"""


# except:
#    print("error")
#    sys.exit(84)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
