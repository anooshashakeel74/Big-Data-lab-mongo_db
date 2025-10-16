import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from dotenv import load_dotenv

load_dotenv()

class MongoDB:
    def __init__(self):
        self.host = os.getenv('MONGO_HOST', 'localhost')
        self.port = int(os.getenv('MONGO_PORT', 27017))
        self.username = os.getenv('MONGO_USERNAME', 'admin')
        self.password = os.getenv('MONGO_PASSWORD', 'password')
        self.database_name = os.getenv('DATABASE_NAME', 'inventory_db')
        self.collection_name = os.getenv('COLLECTION_NAME', 'products')
        
        self.client = None
        self.database = None
        self.collection = None
        
    def connect(self):
        """Establish connection to MongoDB"""
        try:
            connection_string = f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/"
            self.client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB")
            
            self.database = self.client[self.database_name]
            self.collection = self.database[self.collection_name]
            self.collection.create_index("serial_number", unique=True)
            
            return True
            
        except ConnectionFailure:
            print("Failed to connect to MongoDB")
            return False
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            return False
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("📡 MongoDB connection closed")
    
    def get_collection(self):
        """Get the products collection"""
        return self.collection