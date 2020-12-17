import pymongo


class Database:
    client = pymongo.MongoClient()  # Insert your mongoDB credentials
    schools_db = client.Cluster0
    schools_collection = schools_db.get_collection("schools")
    database = schools_collection

    def connect_db(self):
        if self.client is not None:
            return self.client
        else:
            raise Exception("Can not connect the DB")

    def close_db(self):
        self.client.close()

    def get_database(self):
        return self.database
