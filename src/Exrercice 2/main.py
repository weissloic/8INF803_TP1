import pymongo
import json

def main():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    graph = {
        "id": "Page_A",
        "value": {
            "pageRank": "1",
            "adjlist": ["Page_B", "Page_C"]
        }
    }




if __name__ == "__main__":
    main()