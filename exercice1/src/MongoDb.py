from bson import Code
from pymongo import MongoClient


class MongoDB:

    def __init__(self):
        self.client = MongoClient("mongodb://root:rootpassword@localhost:27017")
        self.db = self.client.business

    def map_reduce_request(self):
        collection = self.db.reviews

        map = Code("function () {"
                   "  var level_wiz;"
                   "if (this.components.includes('V') && this.components.length == 1) {"
                   "if (this.class_linked.includes('wizard')) {"
                   " level_wiz = this.class_linked.split('wizard ')[1];"
                   "if (parseInt(level_wiz) <= 4)"
                   " emit(this.name, this.components)"
                   "}"
                   "}"
                   "}")

        reduce = Code("function (key, values) {"
                      "  var total = 0;"
                      "  for (var i = 0; i < values.length; i++) {"
                      "    total += values[i];"
                      "  }"
                      "  return total;"
                      "}")

        result = collection.map_reduce(map, reduce, "myresults")
        counter = 0

        for doc in result.find():
            counter += 1
            print(doc)
