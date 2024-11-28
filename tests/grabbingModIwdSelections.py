import os

wawRootDir = r'D:\SteamLibrary\steamapps\common\Call of Duty World at War'
modsDir = os.path.join(wawRootDir, 'mods')
modName = 'zm_test1'
modDir = os.path.join(modsDir, modName)

modIwdContents = {}

def grabModStructure(root_dir: str=os.getcwd(), files_to_ignore: list=[], folders_to_ignore: list=[], indent: int=0) -> dict:
    structure = {}
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        if os.path.isdir(item_path):
            if any(folder in item for folder in folders_to_ignore):
                continue
            # Recursively build the folder structure
            structure[item] = grabModStructure(item_path, files_to_ignore, folders_to_ignore, indent + 1)
        else:
            if any(file_name in item for file_name in files_to_ignore):
                continue
            # Store the file in the dictionary
            structure[item] = None
    return structure

def printNicely(structure, indent: int=0) -> None:
    for key, value in structure.items():
        if isinstance(value, dict):
            print("  " * indent + f"📁 {key}")
            printNicely(value, indent + 1)  # Recursively print the nested dictionary (sub-folder)
        else:
            print("  " * indent + f"📄 {key}")  # It's a file, print the file name

def iterateFiles(data, parent='', print_files=False, action=None):
    for key, value in data.items():
        current_path = f"{parent}/{key}" if parent else key  # Join parent with current folder/file
        if isinstance(value, dict):  # If value is a dictionary, recurse
            iterateFiles(value, current_path, print_files, action)
        else:  # If it's a file (None in this case), print the path
            if print_files:
                print(current_path)

            if action:
                action(current_path)

if __name__ == "__main__":
    try:
        modIwdContents = grabModStructure(
            root_dir=modDir,
            folders_to_ignore=['sound']
        )
        printNicely(modIwdContents)

        # iterateFiles(modIwdContents, print_files=True)
    except Exception as e:
        print(e)