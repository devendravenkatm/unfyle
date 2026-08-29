import json
from pathlib import Path

print("==================")
print("      UNFYLE")
print("==================")

document_list = []

choice = 0

def add_document(document_list):
    print("1. Add Documents Selected")
    file_path = input("Enter the file path:")
    file = Path(file_path)
    print("Name:",file.name)
    print("Type:",file.suffix)
    print("Exists:",file.exists())
    if file.exists():
        print("Size:",file.stat().st_size)
        document = {"Name": file.name , "Type" : file.suffix, "Size" : file.stat().st_size }
        print("Document added: ", document)
        document_list.append(document)
        return True
    else:
        print("File not Found")
        return False
        
def list_documents(document_list):
    print("2. List Documents Selected")
    if len(document_list) == 0:
        print("No Documents Found")
    else:
        i = 0
        for document in document_list:
            i += 1
            print(i, document["Name"], document["Type"], document["Size"])

def search_documents(document_list):
    print("3. Search Documents Selected")
    s = input("Enter document name to search: ")
    found = False
    for document in document_list:
        if s.lower() in document["Name"].lower():
            print(document)
            found = True
    if found is False:  
        print("No Documents Found.")

def save_documents(document_list):
    with open("documents.json", "w") as file:
        json.dump(document_list, file)

def load_documents():
    with open("documents.json", "r") as file:
        return json.load(file)

try :
    document_list = load_documents()
except FileNotFoundError:
    document_list = []



while choice != '4':
   print("1. Add Document")
   print("2. List Documents")
   print("3. Search Documents")
   print("4. Exit")
   choice = input("Choose an option: ")
   if choice == '1':
      result = add_document(document_list)
      if result:
          save_documents(document_list)
   elif choice == '2':
      list_documents(document_list)
   elif choice == '3':
      search_documents(document_list)
   elif choice == '4':
      print("4. Exit")
   else:
      print("Invalid")
   