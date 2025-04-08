from DB import DB, os
import re

class Main:
    def main(self):
        pwd = input("Enter password: ")

        db = DB(pwd)

        db.useDB("test")

        try:
            while True:
                command = input(f"[{db.currentDB}]> ").strip()

                # Extract content inside parentheses
                bracket_content = re.findall(r"\((.*?)\)", command)

                # Split the command at spaces and dots, ignoring content inside parentheses
                command_without_brackets = re.sub(r"\(.*?\)", "", command)  # Remove bracket content
                parts = re.split(r"[ .]+", command_without_brackets.strip())


                if not parts:
                    continue  # Skip empty input

                main_command = parts[0]  # The first keyword

                # Process commands
                if main_command == "db" and len(parts) > 1 and parts[1] == "createCollection":
                    if bracket_content:
                        collection_name = bracket_content[0]  # Take first value inside parentheses
                        db.createCollection(collection_name)
                    else:
                        db.createCollection("default_collection")  # Default name if none given
                elif main_command == "show" and len(parts) > 1:
                    if parts[1] == "dbs":
                        db.showDBs()
                    elif parts[1] == "collections":
                        db.showCollections()
                    else:
                        continue
                elif main_command == "db" and len(parts) > 2 and parts[2] == "find":
                    db.find(parts[1], str(bracket_content[0]) if bracket_content else "{}")
                elif main_command == "db" and len(parts) > 2 and parts[2] == "insertOne":
                    db.insertOne(parts[1], str(bracket_content[0]))
                elif main_command == "use" and len(parts) > 1:
                    db.useDB(parts[1])
                elif main_command in ("cls", "clear"):
                    os.system("cls")
                elif main_command == "exit":
                    print("Exiting...")
                    break  # Exit the loop
                else: 
                    continue  # Skip invalid command

        except KeyboardInterrupt:
            print("\nExiting...")
            exit(0)



if __name__ == "__main__":
    main = Main()
    main.main()