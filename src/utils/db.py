import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

class DatabaseClient:

    def __init__(self, uri):
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.database = self.client["facebook"]
        
        pingSuccesfull = False
        while pingSuccesfull == False:
            try:
                self.client.admin.command('ping')
                now = datetime.now().strftime('%H:%M:%S')
                print(f"{now} utils.Database: Pinged your deployment. You successfully connected to MongoDB!")
                pingSuccesfull = True
            except Exception:
                now = datetime.now().strftime('%H:%M:%S')
                print(f"{now} utils.Database: You cannot connect to MongoDB. Retrying...")

    def _insert_url(self, list_url, type):
        now = datetime.now().strftime('%H:%M:%S')
        print(f"{now} utils.Database: Inserting url to collection, please wait...")
        listOfDucuments = [{'type': type, 'url': url} for url in list_url]
        urlCollection = self.database.get_collection("url_list")
        urlCollection.insert_many(listOfDucuments)

