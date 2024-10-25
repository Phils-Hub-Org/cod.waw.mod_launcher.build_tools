""" NOTE
(1):
    When testing, you will need to replace the below 'wawRootDir' with your actual WAW root directory
    as well as the 'modName' with the actual name of your mod.

(2):
    The default stock mod launcher behaviour is to copy mod.ff to appdata/mods folder if it is not present there during the iwd stage.
    So this module does take care of that, but for the actual building of the mod.ff, check out the 'build_mod_ff.py' module.

For output information refer to: 'Misc/building-iwd-info.txt'
"""

import os, sys, shutil, zipfile

def build(modName: str, modDir: str, activisionModDir: str, foldersToIgnore: list=[], filesToIgnore: list=[], printFunc=print) -> None:
    # function calls
    steps = [
        # NOTE: Even though we're not using the stock 7za.exe anymore, may as well keep the output looking familiar.
        lambda arg1='7-Zip (A) 4.42  Copyright (c) 1999-2006 Igor Pavlov  2006-05-14': printFunc(arg1),
        lambda arg1='Scanning': printFunc(arg1),
        lambda arg1=f'Creating archive {os.path.join(modDir, f'{modName}.iwd')}': printFunc(arg1),

        lambda arg1=modDir, arg2=modName, arg3=foldersToIgnore, arg4=filesToIgnore, arg5=printFunc: buildIwd(arg1, arg2, arg3, arg4, arg5),
        lambda arg1=modName, arg2=modDir, arg3=activisionModDir, arg4=printFunc: copyModIwdFromModToActivisionMod(arg1, arg2, arg3, arg4),
        lambda arg1=activisionModDir, arg2=modDir, arg3=printFunc: copyModFfFromModToActivisionMod(arg1, arg2, arg3),
        lambda arg1='Everything is Ok': printFunc(arg1),
    ]

    for step in steps:
        try:
            step()
        except Exception as error:
            teardown(message=f"Step {step.__name__} failed: {error}", printFunc=printFunc)

def buildIwd(modDir: str, modName: str, foldersToIgnore: list, filesToIgnore: list, printFunc=print) -> None:
    # Anything to be built into the modname.iwd will need its full mod dir path (exluding leading up to mod root).
    array = []

    itemsToPkgIntoIwd = grabModStructure(
        rootDir=modDir,
        foldersToIgnore=foldersToIgnore,
        filesToIgnore=filesToIgnore
    )

    iterateFiles(data=itemsToPkgIntoIwd, action=lambda x: array.append(x), printFunc=printFunc)

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

            printFunc(f'Compressing  {item}')
            
            # Add the file to the zip archive
            zipf.write(file_to_add, file_in_iwd)

# Utilized by: buildIwd()
def grabModStructure(rootDir: str=os.getcwd(), foldersToIgnore: list=[], filesToIgnore: list=[]) -> dict:
    structure = {}
    for item in os.listdir(rootDir):
        item_path = os.path.join(rootDir, item)
        if os.path.isdir(item_path):
            if any(folder in item for folder in foldersToIgnore):
                continue
            # Recursively build the folder structure
            structure[item] = grabModStructure(item_path, filesToIgnore, foldersToIgnore)
        else:
            if any(fileName in item for fileName in filesToIgnore):
                continue
            # Store the file in the dictionary
            structure[item] = None
    return structure

# Utilized by: buildIwd()
def iterateFiles(data: dict, action: callable=None, printFunc=print, parent: str='') -> None:
    for key, value in data.items():
        current_path = f"{parent}/{key}" if parent else key  # Join parent with current folder/file
        if isinstance(value, dict):  # If value is a dictionary, recurse
            iterateFiles(data=value, action=action, printFunc=printFunc, parent=current_path)
        else:  # If it's a file (None in this case), print the path
            if action:
                action(current_path)

def copyModIwdFromModToActivisionMod(modName: str, modDir: str, activisionModDir: str, printFunc=print) -> None:
    modIwdSource = os.path.join(modDir, f'{modName}.iwd')
    modIwdDest = os.path.join(activisionModDir, f'{modName}.iwd')

    if not os.path.exists(activisionModDir):
        os.makedirs(activisionModDir)

    shutil.copy2(modIwdSource, modIwdDest)

    printFunc(f"Copying  {modIwdSource}")
    printFunc(f"     to  {modIwdDest}")

def copyModFfFromModToActivisionMod(activisionModDir: str, modDir: str, printFunc=print) -> None:
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

            printFunc(f"Copying  {modFfSource}")
            printFunc(f"     to  {modFfDest}")

def teardown(message: str='[build_iwd.py]: Something went wrong...', printFunc=print) -> None:
    printFunc(message)
    sys.exit(1)

# Example usage
if __name__ == '__main__':
    # change these 2 as needed
    # NOTE: Be careful with variables that are in global scope like the below 2.
    #       I change their styling from the args styling so function couldn't utilize them as they should be passed in as args.
    mod_name = 'zm_test1'
    waw_root_dir = r'D:\SteamLibrary\steamapps\common\Call of Duty World at War'    

    print()  # to separate from vs output
    build(
        modName=mod_name,
        modDir=os.path.join(os.path.join(waw_root_dir, 'mods'), mod_name),
        activisionModDir=os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Activision', 'CoDWaW', 'mods', mod_name),  # '~' = home dir
        foldersToIgnore=[
            'sound',
        ],
        filesToIgnore=[
            'mod.ff',
            f'{mod_name}.files',
            f'{mod_name}.iwd',
            'console.log',
        ],
        # printFunc=print  # the build func already utilizes print as the default output, so only use this arg when wanting to handle the output differently.
    )
    print()  # to separate from vs output
