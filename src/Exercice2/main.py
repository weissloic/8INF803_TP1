from pymongo import MongoClient
from bson.code import Code

def main():
    # Connection to DB
    client = MongoClient('localhost', 27017)
    db = client.exercice2
    collection = db.graphPR
    collection.delete_many({})
    # Init data with pageRank = 1
    graph = [
        {"_id": "A", "value": {"pageRank": 1, "adjList": ["B", "C"]}},
        {"_id": "B", "value": {"pageRank": 1, "adjList": ["C"]}},
        {"_id": "C", "value": {"pageRank": 1, "adjList": ["A"]}},
        {"_id": "D", "value": {"pageRank": 1, "adjList": ["C"]}}
    ]
    collection.insert_many(graph)

    for i in range(0,21):
        print("VALEUR DE I : " + str(i))
        map = Code("function () {"
                "  var key;"
                "  var count = 0;"
                "  for(key in this.value.adjList) {"
                "        count++;"
                "    }"
                "  PrValue = this.value.pageRank;"
                "  this.value.adjList.forEach(function(id) {"
                "    emit(id, PrValue/count);"
                "    });"
                " emit(this._id, this.value.adjList)"
                "}")

        reduce = Code("function (key, value) {"
                    "  const DAMPING_FACTOR = 0.85;"
                    "  var resultTab = {"
                    "  pageRank:'',"
                    "  adjList:'' };"
                    "  var somme = 0;"
                    "  var newPR = 0;"
                    "  for (let i = 0; i < value.length; i++){ "
                    "       if(!isNaN(value[i])){ "
                    "         somme += value[i]"
                    "             }"
                    "       else{"
                    "          resultTab.adjList = value[i];"
                    "         }"
                    "       }"
                    "  newPR = (1-DAMPING_FACTOR) + DAMPING_FACTOR*somme;"
                    "  resultTab.pageRank = newPR;"
                    "  return resultTab;"
                    "}")
        result = collection.map_reduce(map, reduce, "myresults")
        collection.delete_many({})
        resultTab = []
        for doc in result.find():
            resultTab.append(doc)
            print(doc)
        collection.insert_many(resultTab)
        print("***********************************************************************************")
        print("***********************************************************************************")
        print("***********************************************************************************")


if __name__ == "__main__":
    main()