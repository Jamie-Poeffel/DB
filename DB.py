import os
import bson
from converters import PWD, Encrypt
import uuid
import json

class DB:
    currentDB = ""

    def __init__(self, pwd):
        print("connected DB")
        
        if not os.path.exists("db"):
            os.mkdir("db")
        
        if not os.path.exists("db/admin.bson"):
            with open("db/admin.bson", "wb") as f:
                data = {"account": "admin", "pwd": PWD.hash_password(pwd)}
                bson_data = bson.dumps(data)
                f.write(bson_data)
        else:
            with open("db/admin.bson", "rb") as f:
                data = f.read()
                bson_data = bson.loads(data)
                if not PWD.check_password(bson_data["pwd"], pwd):
                    print("Wrong password")
                    exit(1)




    def useDB(self, name):
        self.currentDB = name



    def showDBs(self):
        db_path = "db/"
        if not os.path.exists(db_path):
            print("Database directory not found.")
            return
        
        count = 0
        for folder in os.scandir(db_path):
            if folder.is_dir():
                size, unit = self.get_folder_size(folder.path)
                print(f"{folder.name} -> {size:.2f} {unit}")
                count += 1
            
        if count == 0:
            print("\r")





            

    def get_folder_size(self, path):
        total_size = sum(
            os.path.getsize(os.path.join(dirpath, file))
            for dirpath, _, filenames in os.walk(path)
            for file in filenames
            if os.path.exists(os.path.join(dirpath, file))
        )

        # Determine the appropriate unit
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if total_size < 1024:
                return total_size, unit
            total_size /= 1024

        return total_size, "TB"






    def showCollections(self):
        if os.path.exists("db/" + self.currentDB):
            for file in os.scandir("db/" + self.currentDB):
                if file.is_file() and file.name.endswith(".bson"):
                    print(file.name[:-5])
        else:
            print("Database not found")





    def find(self, collection, query={}):
        db_path = f"db/{self.currentDB}/{collection}.json"
        config = f"db/{self.currentDB}/{collection}.bson"
        key = ""

        if os.path.exists(db_path):
            all_data = []
            try:
                with open(config, "rb") as f:
                    data = f.read()

                    try:
                        bson_data = bson.loads(data)
                        if "key" not in bson_data:
                            print("Collection not found")
                            return
                        key = bson_data["key"]
                    except bson.errors.BSONError as e:
                        print(f"Error loading BSON data: {e}")
                        return

                    with open(db_path, "r") as f:
                        try:
                            file_data = f.read()
                            json_data = list(json.loads(file_data))

                            if not isinstance(json_data, list):
                                json_data = []
                        except json.JSONDecodeError as e:
                            print(f"Error loading JSON data: {e}")
                            json_data = []

                    for jso in json_data:
                        try:
                            decrypted_data = Encrypt.dual_decrypt(jso["data"],  f"{self.currentDB}{collection}", key)
                            try:
                                parsed_data = json.loads(decrypted_data)
                            except json.JSONDecodeError:
                                parsed_data = decrypted_data  
                                
                            all_data.append({
                                "_id": jso["_id"],
                                "data": parsed_data
                            })
                        except Exception as e:
                            print(f"Error decrypting data: {e}")
                            continue

                    if query != {}:
                        print(json.dumps(all_data, indent=4, ensure_ascii=False))
                    else:
                        print(json.dumps(all_data, indent=4, ensure_ascii=False))
            except Exception as e:
                print(f"Error reading collection: {e}")
                return





    def createCollection(self, name):
        if not os.path.exists(f"db/{self.currentDB}"):
            os.mkdir(f"db/{self.currentDB}")
        if not os.path.exists(f"db/{self.currentDB}/{name}.bson"):
            with open(f"db/{self.currentDB}/{name}.bson", "wb") as f:
                data = {"key": str(uuid.uuid4())}
                bson_data = bson.dumps(data)
                f.write(bson_data)
            with open(f"db/{self.currentDB}/{name}.json", "w") as f:
                f.write("[]")  
        else:
            print("Collection already exists")




    def insertOne(self, collection, data):
        db_path = f"db/{self.currentDB}/{collection}.json"
        config_path = f"db/{self.currentDB}/{collection}.bson"
        key = ""

        if os.path.exists(db_path) and os.path.exists(config_path):
            try:
                with open(config_path, "rb") as f:
                    config_bytes = f.read()  
                    bson_data = bson.loads(config_bytes)
                    if "key" not in bson_data:
                        print("Key not found in config")
                        return
                    key = bson_data["key"]

                with open(db_path, "r", encoding="utf-8") as f:
                    try:
                        json_data = json.load(f)
                        if not isinstance(json_data, list):
                            json_data = []
                    except json.JSONDecodeError:
                        json_data = []

                encrypted_data = Encrypt.dual_encrypt(data, f"{self.currentDB}{collection}", key)

                new_entry = {
                    "_id": str(uuid.uuid4()),
                    "data": encrypted_data
                }
                json_data.append(new_entry)

                with open(db_path, "w", encoding="utf-8") as f:
                    json.dump(json_data, f, indent=4)

                print("1 succeeded, 0 failed to insert")
            except Exception as e:
                print(f"Error writing to collection: {e}")
                print("0 succeeded, 1 failed to insert")
        else:
            print("Collection not found")