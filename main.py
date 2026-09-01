import json
from pathlib import Path
import pymupdf

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
    print("Path:",file_path)
    if file.exists():
        if file.suffix.lower() == ".pdf":
            print("Size:",file.stat().st_size)
            extracted_text = extract_file(file_path)
            document = {"Name": file.name , "Type" : file.suffix, "Size" : file.stat().st_size, "Path" : file_path, "Text" : extracted_text}
            print("Document added: ", document)
            document_list.append(document)
            return True
        else:
            print("Unsupported file format")
            return False
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
            size_kb = document["Size"]/1024
            print(i, document["Name"], document["Type"], f"{size_kb:.2f}KB")

def extract_file(file_path):
    text_list = []
    pdf = pymupdf.open(file_path)
    for page in pdf:
        text = page.get_text()
        text_list.append(text)
    return text_list

def search_documents(document_list):
    print("3. Search Documents Selected")
    s = input("Enter text to search: ")
    found = False
    for document in document_list:
        if "Text" in document:
            text_list = document["Text"]
        else:
            text_list = extract_file(document["Path"])
        for i,page_text in enumerate(text_list, start = 1):
            for line in page_text.splitlines():
                if s.lower() in line.lower():
                    print(document["Name"])
                    print(f"Found on page {i}", line)
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

def edit_documents(document_list):
    if len(document_list) == 0:
        print("Invalid Document Number")
        return
    list_documents(document_list)
    try:
        r = int(input("Enter the document number to edit: "))
    except ValueError:
        print("Invalid document number")
        return
    if r < 1 or r > len(document_list):
        print("Invalid document number")
        return
    index1 = r - 1
    document = document_list[index1]
    file = Path(document["Path"])
    new_name = input("Enter the name: ")
    new_path = file.parent/new_name
    file.rename(new_path)
    document["Name"] = new_name
    document["Path"] = str(new_path)
    print("Document Renamed Successfully")


def delete_documents(document_list):
    if len(document_list) == 0:
        print("No Documents Found")
        return
    list_documents(document_list)
    try:
        d = int(input("Enter the document number to delete: "))
    except ValueError:
        print("Please enter a valid number")
        return
    if d < 1 or d > len(document_list):
        print("Invalid number")
        return
    index = d - 1
    deleted_document = document_list.pop(index)
    print("Document deleted:", deleted_document)
        


while choice != '6':
   print("1. Add Document")
   print("2. List Documents")
   print("3. Search Documents")
   print("4. Edit Documents")
   print("5. Delete Documents")
   print("6. Exit")
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
       edit_documents(document_list)
       save_documents(document_list)
   elif choice == '5':
      delete_documents(document_list)
      save_documents(document_list)
   elif choice == '6':
       print("6. Exit")
   else:
      print("Invalid")
   