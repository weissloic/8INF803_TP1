import urllib.request as req

class Spell:
    def __init__(self, name):
        self.name = name
        self.classLinked = ""
        self.components = []
        self.level = None
        self.resistance = None
        self.url = req.pathname2url(name)#name.replace(" ", "%20").replace("'", "%27")