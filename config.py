import os, argparse

parser = argparse.ArgumentParser()
parser.add_argument("--db-connection-string", nargs="?", action="store", dest="db_connection_string", help="The MongoDB ConnectionString")
parser.add_argument("--db-database-id", nargs="?", action="store", dest="db_database_id", help="The MongoDB Database ID")
parser.add_argument("--db-collection-id", nargs="?", action="store", dest="db_collection_id", help="The MongoDB Collection ID")

class Config(object):
    def __init__(self):
        args = parser.parse_args()

        self.DB_CONNECTIONSTRING = os.environ.get("DB_CONNECTIONSTRING")
        if not self.DB_CONNECTIONSTRING:
            if not args.db_connection_string:
                raise ValueError("No DB_CONNECTIONSTRING set in CLI arguments or OS Environment")
            self.DB_CONNECTIONSTRING = args.db_connection_string

        self.DB_DATABASE_ID = os.environ.get("DB_DATABASE_ID")
        if not self.DB_DATABASE_ID:
            if not args.db_database_id:
                raise ValueError("No DB_DATABASE_ID set in CLI arguments or OS Environment")
            self.DB_DATABASE_ID = args.db_database_id

        self.DB_COLLECTION_ID = os.environ.get("DB_COLLECTION_ID")
        if not self.DB_COLLECTION_ID:
            if not args.db_collection_id:
                raise ValueError("No DB_COLLECTION_ID set in CLI arguments or OS Environment")
            self.DB_COLLECTION_ID = args.db_collection_id
