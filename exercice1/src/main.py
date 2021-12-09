import sys
import re
from Spell import *
from SqLite import *

from Parsing import *

from MongoDb import *
from Utils import *
import os

import json

def getComponent(find_infos):
    print("Components: " + find_infos.group(4))

    tmpComponent = find_infos.group(4)
    if tmpComponent.find('('):
        tmpComponent = re.sub(r"\([^()]*\)", "", find_infos.group(4))

    listComp = tmpComponent.split(",")
    listComp = [x.strip(' ') for x in listComp]
    #print(listComp)

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

    tmp = re.sub(r"\([^()]*\)", "", find_infos.group(2))

    return tmp

def fill_file(spell):

    a = []
    filename = 'myFile.json'

    if not os.path.isfile(filename):
        a.append(spell)
        with open(filename, mode='w') as f:
            f.write(json.dumps(a, indent=2))
    else:
        with open(filename) as feedsjson:
            feeds = json.load(feedsjson)

        feeds.append(spell)
        with open(filename, mode='w') as f:
            f.write(json.dumps(feeds, indent=2))

def parsePage(mongo, prs, sqLite):
    sqLite.drop_table()
    soup = prs.init_soup("Spells.aspx?Class=All")

    for url in soup.find_all('td'):
        spell_class = Spell(prs.get_spell_name(url))
        #spell_class = Spell("Dimension Door")
        soup = prs.init_soup("SpellDisplay.aspx?ItemName=" + spell_class.url)


        spellDiv = soup.find(id="ctl00_MainContent_DataListTypes")



        if "(" in spell_class.name:
            spell_class.name = spell_class.name.replace("(", "\(").replace(")", "\)")

        #print(spellDiv)
        #"Absorb Rune II.*?(<.*?Description<\/h3>).*?(PFS)"
        #Absorb Rune III.*?(<.*?Description<\/h3>).*(<\/)
        desc = spell_class.name + ".*?(<.*?Description<\/h3>)(.*)?(PFS)"
        desc2 = spell_class.name + ".*?(<.*?Description<\/h3>)(.*)(<\/spa)"

        spellDiv = str(spellDiv).replace("\n", "")
        findDesc = re.search(desc, str(spellDiv))

        description = ""

        if findDesc != None:
            description = findDesc.group(2)
        else:
            findDesc2 = re.search(desc2, str(spellDiv))
            if (findDesc2 != None):
                description = findDesc2.group(2)




        regex = spell_class.name + "<\/h1>.*(Level<\/b>(.*?))<.*Description<\/h3>"

        find_infos = re.search(regex, str(spellDiv))

        if find_infos:
            regex = prs.get_nice_parsing(find_infos, spell_class.name)


            print("name class: " + spell_class.name)
            find_infos = re.search(regex, str(spellDiv))
            #print(find_infos.group(1))
            #print(re.sub(r"\([^()]*\)", "", find_infos.group(2)))

            spell_class.classLinked = getClassLinked(find_infos)
            spell_class.level = getLevel(spell_class.classLinked, prs)
            spell_class.components = getComponent(find_infos)
            spell_class.resistance = getResistance(find_infos, prs.spell_found)



            spell = {
                'name': spell_class.name,
                'level': spell_class.level,
                'url': "https://aonprd.com/SpellDisplay.aspx?ItemName=" + spell_class.url,
                'des': description,
                'class_linked': spell_class.classLinked,
                'components': spell_class.components,
                'spell_resistance': spell_class.resistance
            }

            print(spell)
            fill_file(spell)

            #mongo.db.reviews.insert_one(spell)
            #print("data put in mongoBD")
            #sqLite.put_spell(spell_class)
            #result = mongo.db.reviews.insert_one(spell)

        else:
            prs.counter_error += 1


        print("error: ", prs.counter_error)
        print("spell not displayed: ", prs.counter_spell_not_displayed)
        print("---------------------------------\n")


def fill_db_file(mongo, sqLite):
    filename = 'myFile.json'
    sqLite.drop_table()
    with open(filename) as feedsjson:
        feeds = json.load(feedsjson)

    for spell in feeds:
        spell_class = Spell(spell["name"])
        spell_class.level = spell["level"]
        spell_class.classLinked = spell["class_linked"]
        spell_class.components = spell["components"]
        spell_class.resistance = spell["spell_resistance"]

        mongo.db.reviews.insert_one(spell)
        print("data put in mongoBD")
        sqLite.put_spell(spell_class)

def menu(mongo, prs, sqLite):

    print('Select the operation to do:')
    print('1: Parse the page and fill the DB')
    print('2: Execute MongoDB Map Reduce (make sure MDB is filled)')
    print('3: Execute SQL Request (make sure SQL is filled)')
    print('4: Fill the DBs with an example file')
    print('5: Exit the program')
    x = input()

    print('\n')

    if int(x) == 1:
        parsePage(mongo, prs, sqLite)
    if int(x) == 2:
        mongo.map_reduce_request()
    if int(x) == 3:
        sqLite.select_spell()
    if int(x) == 4:
        fill_db_file(mongo, sqLite)
    if int(x) == 5:
        sys.exit(0)


    print('\n---------------------------\n')

    menu(mongo, prs, sqLite)

def main(args):
    # try:

    tt = Utils()
    prs = Parsing()

    mongo = MongoDB()
    sqLite = SqLite("spell.db")

    menu(mongo, prs, sqLite)

# except:
#    print("error")
#    sys.exit(84)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
