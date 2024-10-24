r""" STOCK MOD LAUNCHER OUTPUT
WHEN mod.ff is present in AppData
    Actual Outut: (Although the order is a bit janky (copying output should be seen last) imo, so ill ensure that the output looks clearer).
        7-Zip (A) 4.42  Copyright (c) 1999-2006 Igor Pavlov  2006-05-14
        Copying  D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\zm_tst1.iwd
            to  C:\Users\Phil-\AppData\Local\Activision\CodWaW\mods\zm_tst1\zm_tst1.iwd
        Scanning

        Creating archive D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\zm_tst1.iwd

        Compressing  mod.csv

        Everything is Ok

    My Output:
        7-Zip (A) 4.42  Copyright (c) 1999-2006 Igor Pavlov  2006-05-14
        Scanning

        Creating archive D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\zm_tst1.iwd

        Compressing  mod.csv

        Copying  D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\zm_tst1.iwd
            to  C:\Users\Phil-\AppData\Local\Activision\CodWaW\mods\zm_tst1\zm_tst1.iwd

        Everything is Ok

WHEN mod.ff is NOT present in AppData
    Actual Outut: (Again, the order is a bit janky, so ill be sure to correct it in my version).
        7-Zip (A) 4.42  Copyright (c) 1999-2006 Igor Pavlov  2006-05-14
        Scanning
        Copying  D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\mod.ff
            to  C:\Users\Phil-\AppData\Local\Activision\CodWaW\mods\zm_tst1\mod.ff
        Copying  D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\zm_tst1.iwd
            to  C:\Users\Phil-\AppData\Local\Activision\CodWaW\mods\zm_tst1\zm_tst1.iwd

        Creating archive D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\zm_tst1.iwd

        Compressing  mod.csv

        Everything is Ok

    My Output:
        7-Zip (A) 4.42  Copyright (c) 1999-2006 Igor Pavlov  2006-05-14
        Scanning

        Creating archive D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\zm_tst1.iwd

        Copying  D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\zm_tst1.iwd
            to  C:\Users\Phil-\AppData\Local\Activision\CoDWaW\mods\zm_tst1\zm_tst1.iwd

        Copying  D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\mod.ff
            to  C:\Users\Phil-\AppData\Local\Activision\CoDWaW\mods\zm_tst1\mod.ff

        Everything is Ok
"""

""" NOTE
(1):
    mod.ff only gets copied to mods > appdata if its not present in the appdata/mods folder.
    The actual compiling of the mod.ff file is obv not done here.

(2):
    When testing, you will need to replace the below 'wawRootDir' with your actual WAW root directory, as well as the 'MOD_NAME' with the actual name of your mod.

Below vars:
    UPPERCASE: Used globally (scope: module) and locally (scope: function)
    lowercase: used globally (scope: module)
"""

import os, sys, shutil, zipfile

WAW_ROOT_DIR = r'D:\SteamLibrary\steamapps\common\Call of Duty World at War'
MODS_DIR = os.path.join(WAW_ROOT_DIR, 'mods')
MOD_NAME = 'zm_tst1'
MOD_DIR = os.path.join(MODS_DIR, MOD_NAME)

homeDir = os.path.expanduser('~')
appdataDir = os.path.join(homeDir, 'AppData')
activisionDir = os.path.join(appdataDir, 'Local', 'Activision')
activisionModsDir = os.path.join(activisionDir, 'CoDWaW', 'mods')
ACTIVISION_MOD_DIR = os.path.join(activisionModsDir, MOD_NAME)

def buildIwd():
    # print(f'\nBuild iwd start')
    # print(f"############################## ---/--/--- ##############################\n")
    
    # Anything to be built into the modname.iwd will need its full mod dir path (exluding leading up to mod root).
    array = []

    itemsToPkgIntoIwd = grabModStructure(
        root_dir=MOD_DIR,
        files_to_ignore=[
            'mod.ff',
            f'{MOD_NAME}.files',
            f'{MOD_NAME}.iwd',
            'console.log',
        ],
        folders_to_ignore=[
            'sound',
        ]
    )

    iterateFiles(itemsToPkgIntoIwd, action=lambda x: array.append(x))

    iwdDest = os.path.join(MOD_DIR, f'{MOD_NAME}.iwd')

    # delete old iwd if it exists
    if os.path.exists(iwdDest):
        os.remove(iwdDest)

    array = sorted(array)  # sort in ascending order

    for item in array:        
        with zipfile.ZipFile(iwdDest, 'a', zipfile.ZIP_DEFLATED) as zipf:  # 'a' for append, just be sure to delete old iwd first
            # Specify files and where you want them in the .iwd archive
            # For example, placing a specific file in the 'aitype' folder inside the iwd
            
            # Full path to the source file on the disk
            file_to_add = os.path.join(MOD_DIR, item).replace('\\', '/')
            # file_to_add = 'D:/SteamLibrary/steamapps/common/Call of Duty World at War/mods/zm_tst1/aitype/axis_zombie_ger_ber_sshonor.gsc'
            
            # Specify the destination path inside the iwd archive (as if you're recreating the folder structure)
            file_in_iwd = item
            # file_in_iwd = 'aitype/axis_zombie_ger_ber_sshonor.gsc'

            print(f'Compressing  {item}')
            
            # Add the file to the zip archive
            zipf.write(file_to_add, file_in_iwd)

    # print(f'\n############################## ---/--/--- ##############################')
    # print(f'Build iwd end\n')

# Utilized by: buildIwd()
def grabModStructure(root_dir: str=os.getcwd(), files_to_ignore: list=[], folders_to_ignore: list=[]) -> dict:
    structure = {}
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        if os.path.isdir(item_path):
            if any(folder in item for folder in folders_to_ignore):
                continue
            # Recursively build the folder structure
            structure[item] = grabModStructure(item_path, files_to_ignore, folders_to_ignore)
        else:
            if any(file_name in item for file_name in files_to_ignore):
                continue
            # Store the file in the dictionary
            structure[item] = None
    return structure

# Utilized by: buildIwd()
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

def copyModIwdFromModToActivisionMod():
    # print(f'\nCopy mod.iwd start')
    # print(f"############################## ---/--/--- ##############################\n")
    
    modIwdSource = os.path.join(MOD_DIR, 'zm_tst1.iwd')
    modIwdDest = os.path.join(ACTIVISION_MOD_DIR, 'zm_tst1.iwd')

    if not os.path.exists(ACTIVISION_MOD_DIR):
        os.makedirs(ACTIVISION_MOD_DIR)

    shutil.copy2(modIwdSource, modIwdDest)

    print(f"Copying  {modIwdSource}")
    print(f"     to  {modIwdDest}")

    # print(f'\n############################## ---/--/--- ##############################')
    # print(f'Copy mod.iwd end\n')

# Just a nice touch that the stock launcher has where it ensures the mod.ff is present in appdata/mods folder during the iwd stage.
def copyModFfFromModToActivisionMod():
    # print(f'\nCopy mod.ff start')
    # print(f"############################## ---/--/--- ##############################\n")

    # if mod.ff is already present in appdata/mods, then return
    if os.path.exists(os.path.join(ACTIVISION_MOD_DIR, 'mod.ff')):
        return
    
    modFfSource = os.path.join(MOD_DIR, 'mod.ff')
    modFfDest = os.path.join(ACTIVISION_MOD_DIR, 'mod.ff')

    if not os.path.exists(ACTIVISION_MOD_DIR):
        os.makedirs(ACTIVISION_MOD_DIR)

    shutil.copy2(modFfSource, modFfDest)

    print(f"Copying  {modFfSource}")
    print(f"     to  {modFfDest}")

    # print(f'\n############################## ---/--/--- ##############################')
    # print(f'Copy mod.ff end\n')

if __name__ == "__main__":
    CLEAN = True  # print()  # adds a newline

    steps = [
        # NOTE: Even though we're not using the stock 7za.exe anymore, may as well keep the output looking familiar.
        lambda: print('7-Zip (A) 4.42  Copyright (c) 1999-2006 Igor Pavlov  2006-05-14'),
        lambda: print('Scanning'),
        lambda: print(f'Creating archive {os.path.join(MOD_DIR, f'{MOD_NAME}.iwd')}'),

        lambda: buildIwd(),
        lambda: copyModIwdFromModToActivisionMod(),
        lambda: copyModFfFromModToActivisionMod(),
        lambda: print('Everything is Ok')
    ]

    print()  # to separate from vs output

    try:
        for step in steps:
            if CLEAN:
                print()
            step()

    except Exception as error:
        print(error)
        sys.exit(1)
    
    print()  # to separate from vs output
