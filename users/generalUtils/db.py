from pymongo import MongoClient


class MongoDBConnection:
    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient("mongodb+srv://sergi-aguilar:Xkx04ax1hUNuQ9eD@mydb.4vrxy.mongodb.net/myDB?retryWrites=true&w=majority")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
