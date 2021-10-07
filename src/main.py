import sys
import re
from Spell import *
from SqLite import *

from Parsing import *

from MongoDb import *
from Utils import *

HTML_PARSER = 'html.parser'

def main(args):
    # try:

    tt = Utils()
    prs = Parsing()

    mongo = MongoDB()
    #mongo.map_reduce_request()
    sqLite = SqLite()


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
            spell_list = ""
            print(re.sub(r"\([^()]*\)", "", find_infos.group(2)))

            tmp = find_infos.group(2)
            if tmp.find('('):
                tmp = re.sub(r"\([^()]*\)", "", find_infos.group(2))
            else:
                tmp = re.sub(r"\([^()]*\)", "", find_infos.group(2))

            spell_list = prs.extract_spell_list(tmp)
            #start = find_infos.group(2).find( '(' )

            print("classe linked:", spell_list)

            spell_class.level = prs.get_minimum_level(spell_list)

            #print("Minimum Level: "+prs.get_minimum_level(spell_list))
            print("Components: " + find_infos.group(4))

            tmpComponent = find_infos.group(4)
            if tmpComponent.find('('):
                tmpComponent = re.sub(r"\([^()]*\)", "", find_infos.group(4))

            print(tmpComponent.split(","))

            spell_class.classLinked = tmp
            spell_class.components = tmpComponent.split(",")


            print("Spells Resistance: ")
            if prs.spell_found:
                print("Spells Resistance: " + find_infos.group(6))
                if "yes" in find_infos.group(6):
                    spell_class.resistance = True
                else:
                    spell_class.resistance = False
            else:
                spell_class.resistance = False


            spell = {
                'name': spell_class.name,
                'level': spell_class.level,
                'class_linked': spell_class.classLinked,
                'components': spell_class.components,
                'spell_resistance': spell_class.resistance
            }

            mongo.db.reviews.insert_one(spell)
            sqLite.put_spell(spell_class)

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
