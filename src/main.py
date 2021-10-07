import sys
import re
from Spell import *
from SqLite import *

from Parsing import *

from MongoDb import *
from Utils import *


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
    #mongo.map_reduce_request()
    sqLite = SqLite()

    #mongo = MongoDB()
    #mongo.map_reduce_request()

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

            mongo.db.reviews.insert_one(spell)
            sqLite.put_spell(spell_class)

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
