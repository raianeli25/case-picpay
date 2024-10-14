from mongomock.mongo_client import MongoClient

class InMemoryDatabase:
    """
    A singleton class that provides an in-memory MongoDB database using
    the mongomock library.

    This class ensures that only one instance of the in-memory database
    is created and reused throughout the application.

    Methods
    -------
    __new__(cls) -> MongoClient:
        Creates or returns the existing in-memory database instance.
        If the instance does not exist, it initializes a new MongoClient
        and retrieves the 'memory_db' database.

    Attributes
    ----------
    _instance : MongoClient
        The singleton instance of the in-memory database.
    """
    _instance = None

    def __new__(cls) -> MongoClient:
        if cls._instance is None:
            client = MongoClient()
            cls._instance = client.get_database('memory_db')
        return cls._instance
