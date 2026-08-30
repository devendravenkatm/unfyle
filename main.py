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
            print(i, document["Name"], document["Type"], document["Size"])

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
   