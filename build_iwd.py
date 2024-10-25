""" NOTE
(1):
    When testing, you will need to replace the below 'wawRootDir' with your actual WAW root directory
    as well as the 'modName' with the actual name of your mod.

(2):
    The default stock mod launcher behaviour is to copy mod.ff to appdata/mods folder if it is not present there during the iwd stage.
    So this module does take care of that, but for the actual building of the mod.ff, check out the 'build_mod_ff.py' module.
"""

import os, sys, shutil, zipfile

def build(modDir: str, zoneSourceDir: str, modName: str, binDir: str, zoneEnglishDir: str, activisionModDir: str, printFunc=None) -> None:
    printHandle = print if printFunc is None else printFunc

    # function calls
    steps = [
        # NOTE: Even though we're not using the stock 7za.exe anymore, may as well keep the output looking familiar.
        lambda arg1='7-Zip (A) 4.42  Copyright (c) 1999-2006 Igor Pavlov  2006-05-14': printHandle(arg1),
        lambda arg1='Scanning': printHandle(arg1),
        lambda arg1=f'Creating archive {os.path.join(modDir, f'{modName}.iwd')}': printHandle(arg1),

        lambda arg1=modDir, arg2=modName, arg3=printHandle: buildIwd(arg1, arg2, arg3),
        lambda arg1=modDir, arg2=activisionModDir, arg3=printHandle: copyModIwdFromModToActivisionMod(arg1, arg2, arg3),
        lambda arg1=activisionModDir, arg2=modDir, arg3=printHandle: copyModFfFromModToActivisionMod(arg1, arg2, arg3),
        lambda arg1='Everything is Ok': printHandle(arg1),
    ]

    for step in steps:
        try:
            step()
        except Exception as error:
            teardown(f"Step {step.__name__} failed: {error}")

def buildIwd(modDir: str, modName: str, printFunc=None) -> None:
    # Anything to be built into the modname.iwd will need its full mod dir path (exluding leading up to mod root).
    array = []

    itemsToPkgIntoIwd = grabModStructure(
        root_dir=modDir,
        files_to_ignore=[
            'mod.ff',
            f'{modName}.files',
            f'{modName}.iwd',
            'console.log',
        ],
        folders_to_ignore=[
            'sound',
        ]
    )

    printHandle = print if printFunc is None else printFunc

    iterateFiles(itemsToPkgIntoIwd, action=lambda x: array.append(x), printFunc=printHandle)

    iwdDest = os.path.join(modDir, f'{modName}.iwd')

    # delete old iwd if it exists
    if os.path.exists(iwdDest):
        os.remove(iwdDest)

    array = sorted(array)  # sort in ascending order

    for item in array:        
        with zipfile.ZipFile(iwdDest, 'a', zipfile.ZIP_DEFLATED) as zipf:  # 'a' for append, just be sure to delete old iwd first
            # Specify files and where you want them in the .iwd archive
            # For example, placing a specific file in the 'aitype' folder inside the iwd
            
            # Full path to the source file on the disk
            file_to_add = os.path.join(modDir, item).replace('\\', '/')
            # file_to_add = 'D:/SteamLibrary/steamapps/common/Call of Duty World at War/mods/zm_tst1/aitype/axis_zombie_ger_ber_sshonor.gsc'
            
            # Specify the destination path inside the iwd archive (as if you're recreating the folder structure)
            file_in_iwd = item
            # file_in_iwd = 'aitype/axis_zombie_ger_ber_sshonor.gsc'

            printHandle(f'Compressing  {item}')
            
            # Add the file to the zip archive
            zipf.write(file_to_add, file_in_iwd)

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
def iterateFiles(data, parent: str='', print_files: bool=False, action: callable=None, printFunc=None) -> None:
    printHandle = print if printFunc is None else printFunc

    for key, value in data.items():
        current_path = f"{parent}/{key}" if parent else key  # Join parent with current folder/file
        if isinstance(value, dict):  # If value is a dictionary, recurse
            iterateFiles(value, current_path, print_files, action, printFunc)
        else:  # If it's a file (None in this case), print the path
            if print_files:
                printHandle(current_path)

            if action:
                action(current_path)

def copyModIwdFromModToActivisionMod(modDir: str, activisionModDir: str, printFunc=None) -> None:
    modIwdSource = os.path.join(modDir, f'{modName}.iwd')
    modIwdDest = os.path.join(activisionModDir, f'{modName}.iwd')

    if not os.path.exists(activisionModDir):
        os.makedirs(activisionModDir)

    shutil.copy2(modIwdSource, modIwdDest)

    printHandle = print if printFunc is None else printFunc

    printHandle(f"Copying  {modIwdSource}")
    printHandle(f"     to  {modIwdDest}")

def copyModFfFromModToActivisionMod(activisionModDir: str, modDir: str, printFunc=None) -> None:
    # Just a nice touch that the stock launcher has where it ensures the mod.ff is present in appdata/mods folder during the iwd stage.
    modFfSource = os.path.join(modDir, 'mod.ff')
    modFfDest = os.path.join(activisionModDir, 'mod.ff')

    if not os.path.exists(activisionModDir):
        os.makedirs(activisionModDir)

    # step 1: check if present in root/mods
    if os.path.exists(modFfSource):
        # print('mod.ff present in root/mods')

        # step 2: check if not present in appdata/mods
        if not os.path.exists(modFfDest):
            # print('mod.ff not in appdata/mods')

            shutil.copy2(modFfSource, modFfDest)

    printHandle = print if printFunc is None else printFunc

    printHandle(f"Copying  {modFfSource}")
    printHandle(f"     to  {modFfDest}")

def teardown(message: str, printFunc=None) -> None:
    print(message) if printFunc is None else printFunc(message)
    sys.exit(1)

# Example usage
if __name__ == '__main__':
    # change these 2 as needed
    modName = 'zm_test1'
    wawRootDir = r'D:\SteamLibrary\steamapps\common\Call of Duty World at War'

    print()  # to separate from vs output
    build(
        modDir=os.path.join(os.path.join(wawRootDir, 'mods'), modName),
        zoneSourceDir=os.path.join(wawRootDir, 'zone_source'),
        modName=modName,
        binDir=os.path.join(wawRootDir, 'bin'),
        zoneEnglishDir=os.path.join(wawRootDir, 'zone', 'english'),
        activisionModDir=os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Activision', 'CoDWaW', 'mods', modName),  # '~' = home dir
        printFunc=print
    )
    print()  # to separate from vs output
