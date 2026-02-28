from pymongo import MongoClient
from pymongo.errors import PyMongoError


class AnimalShelter(object):
    """CRUD operations for Animal collection in MongoDB"""

    def __init__(self, user="aacuser", password="", host="localhost", port=27017,
                 db="aac", col="animals"):
        """
        Initialize MongoDB connection.
        NOTE: authSource=admin is required in Codio for your aacuser account.
        """
        self.client = None
        self.database = None
        self.collection = None

        try:
            uri = f"mongodb://{user}:{password}@{host}:{port}/?authSource=admin"
            self.client = MongoClient(uri)

            self.database = self.client[db]
            self.collection = self.database[col]

            # quick connectivity check
            self.client.admin.command("ping")

        except PyMongoError as e:
            print(f"[ERROR] MongoDB connection failed: {e}")

    # C in CRUD
    def create(self, data):
        """
        Insert a document.
        data must be a dictionary.
        Return True if successful, otherwise False.
        """
        if data is None or not isinstance(data, dict) or len(data) == 0:
            return False

        try:
            result = self.collection.insert_one(data)
            return result.acknowledged
        except PyMongoError as e:
            print(f"[ERROR] Insert failed: {e}")
            return False

    # R in CRUD
    def read(self, query):
        """
        Find documents using query dict.
        Return results as a list if successful, otherwise empty list.
        """
        if query is None or not isinstance(query, dict):
            return []

        try:
            cursor = self.collection.find(query)
            return list(cursor)
        except PyMongoError as e:
            print(f"[ERROR] Read failed: {e}")
            return []
        
        from pymongo.errors import PyMongoError

    # UPDATE
    def update(self, query: dict, new_values: dict) -> int:
        """
        Update document(s) matching query using MongoDB $set.
        Returns number of documents modified.
        """
        if query is None or not isinstance(query, dict) or len(query) == 0:
            return 0
        if new_values is None or not isinstance(new_values, dict) or len(new_values) == 0:
            return 0

        try:
            result = self.collection.update_many(query, {"$set": new_values})
            return result.modified_count
        except PyMongoError as e:
            print(f"[ERROR] Update failed: {e}")
            return 0

    # DELETE
    def delete(self, query: dict) -> int:
        """
        Delete document(s) matching query.
        Returns number of documents deleted.
        """
        if query is None or not isinstance(query, dict) or len(query) == 0:
            return 0

        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except PyMongoError as e:
            print(f"[ERROR] Delete failed: {e}")
            return 0

