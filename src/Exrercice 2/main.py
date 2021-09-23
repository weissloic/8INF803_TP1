from pymongo import MongoClient
from bson.code import Code

def main():
    client = MongoClient('localhost', 27017)
    db = client.exercice2
    collection = db.graphPR
    collection.delete_many({})
    graph = [
        {"_id": "A", "value": {"pageRank": 1, "adjList": ["B", "C"]}},
        {"_id": "B", "value": {"pageRank": 1, "adjList": ["C"]}},
        {"_id": "C", "value": {"pageRank": 1, "adjList": ["A"]}},
        {"_id": "D", "value": {"pageRank": 1, "adjList": ["C"]}}
    ]
    collection.insert_many(graph)

    for i in range(0,21):
        map = Code("function () {"
                "  var key;"
                "  var count = 0;"
                "  for(key in this.value.adjList) {"
                "        count++;"
                "    }"
                "  b = this.value.pageRank;"
                "  this.value.adjList.forEach(function(url) {"
                "    emit(url, b/count);"
                "    });"
                " emit(this._id, this.value.adjList)"
                "}")

        reduce = Code("function (key, value) {"
                    "  var tab = {"
                    "  pageRank:'',"
                    "  adjList:'' };"
                    "  var somme = 0;"
                    "  var newPR = 0;"
                    "  for (let i = 0; i < value.length; i++){ "
                    "       if(!isNaN(value[i])){ "
                    "         somme += value[i]"
                    "             }"
                    "       else{"
                    "          tab.adjList = value[i];"
                    "         }"
                    "       }"
                    "  newPR = 0.15 + 0.85*somme;"
                    "  tab.pageRank = newPR;"
                    "  return tab;"
                    "}")
        result = collection.map_reduce(map, reduce, "myresults")
        collection.delete_many({})
        tab = []
        compteur = 0
        print("VALEUR DE I : " + str(i))
        for doc in result.find():
           tab.append(doc)
           print(doc)
        compteur = compteur+1
        collection.insert_many(tab)


if __name__ == "__main__":
    main()