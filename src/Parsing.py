import requests
from bs4 import BeautifulSoup
import re

from src.main import HTML_PARSER


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
