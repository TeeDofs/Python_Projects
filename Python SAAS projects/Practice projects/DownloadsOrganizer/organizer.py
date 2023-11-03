import os
import re
import shutil
from datetime import datetime

def get_all_files(directory):
    #Create an empty list where we'll store our files
    files_list = []

    #List all items in the directory
    all_items = os.listdir(directory)

    #Loop through the items
    for item in all_items:
        #Construct the full path of the item
        item_full_path = os.path.join(directory, item)

        #Check if this item is a file (and not a directory)
        if os.path.isfile(item_full_path):
            #If it's a file, add it to our files list
            files_list.append(item)

    return files_list

def organize_by_type(directory):
    categories = {
        "Images": [".jpg", ".png", ".gif"],
        "Documents": [".pdf", ".docx", ".txt"],
        "Audio": ["mp3", "wav"],
        #Add more categories as needed
    }

    all_files = get_all_files(directory)

    for file_name in all_files:
        file_extension = os.path.splitext(file_name)[1]

        #Determine the correct folder for the file based on its extension
        folder_name = "Others" #default to Others
        for category, extensions in categories.items():
            if file_extension in extensions:
                folder_name = category
                break

        #Create the folder if it doesn't exist
        folder_path = os.path.join(directory, folder_name)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        #Move the file to the appropriate folder
        old_file_path = os.path.join(directory, file_name)
        new_file_path = os.path.join(folder_path, file_name)
        os.rename(old_file_path, new_file_path)

def reset_folder(directory):
    #List all items in the directory 
    all_items = os.listdir(directory)

    for item in all_items:
        item_full_path = os.path.join(directory, item)

        #If item is a folder, check its contents
        if os.path.isdir(item_full_path):
            for sub_item in os.listdir(item_full_path):
                #Move the files out of categorized folders
                shutil.move(os.path.join(item_full_path, sub_item), directory)

            #Once folder is empty, remove folder
            os.rmdir(item_full_path)
        else:
            #For files, remove the prefix numbers
            new_name = re.sub(r"^\d+ - ", "", item) # This regex finds patterns like "1 - " and removes them
            os.rename(item_full_path, os.path.join(directory, new_name))

def sort_files_by_date(directory):
    all_files = get_all_files(directory)

    #Get a list of files along with their creation date
    files_with_date = [(file, os.path.getctime(os.path.join(directory, file))) for file in all_files]

    #Sort the list based on the creation date
    sorted_files = sorted(files_with_date, key=lambda x: x[1], reverse=True)

    #Rename or re-arrange files in the directory based on this sorted order
    for index, (file, _) in enumerate(sorted_files):
        old_path = os.path.join(directory, file)
        # new_name = f"{index + 1} - {file}"
        new_path = os.path.join(directory, file)
        os.rename(old_path, new_path)

    print("Files sorted successfully")

def sort_files_by_size(directory):
    all_files = get_all_files(directory)

    #Get a list of files along with their size
    files_with_size = [(file, os.path.getsize(os.path.join(directory, file))) for file in all_files]

    #Sort the list based on size
    sorted_files = sorted(files_with_size, key=lambda x:x[1], reverse=True)

    for file in sorted_files:
        old_path = os.path.join(directory, file)
        new_path = os.path.join(directory, file)
        os.rename(old_path, new_path)

    print("Files sorted by size successfully")


def sort_files_alphabetically(directory):
    all_files = get_all_files(directory)

    #Sort the list based on size
    sorted_files = sorted(all_files)

    for file in sorted_files:
        old_path = os.path.join(directory, file)
        new_path = os.path.join(directory, file)
        os.rename(old_path, new_path)

    print("Files sorted alphabetically successfully")



directory = r"C:\Users\Tolud\Desktop\Python Projects\Python SAAS projects\Practice projects\Test Downloads"
reset_folder(directory)
sort_files_by_date(directory)
organize_by_type(directory)