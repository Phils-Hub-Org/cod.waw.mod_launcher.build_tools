""" NOTE
(1):
    When testing, you will need to replace the below 'wawRootDir' with your actual WAW root directory
    as well as the 'modName' with the actual name of your mod.

(2):
    The default stock mod launcher behaviour is to copy mod.ff to appdata/mods folder if it is not present there during the iwd stage.
    So this module does take care of that, but for the actual building of the mod.ff, check out the 'build_mod_ff.py' module.

For console output refer to: 'Misc/building-iwd-info.txt'
"""

import os, shutil, zipfile, platform
from datetime import datetime

stepFailure = False
processInterrupted = False

def build(
        modName: str, modDir: str, activisionModDir: str,
        foldersToIgnore: list=[], filesToIgnore: list=[],
        outputHandle=print,
        onProgramSuccessHandle=None, onProgramFailureHandle=None,
        onProcessInterruptedHandle=None,
        addSpaceBetweenSteps=False
    ) -> None:
    # NOTE: Even though we're not using the stock 7za.exe anymore, may as well keep the output looking familiar.
    # outputHandle('7-Zip (A) 4.42  Copyright (c) 1999-2006 Igor Pavlov  2006-05-14')
    outputHandle(f'Python zipfile (P) {platform.python_version()}')
    outputHandle(f'Copyright (c) 2001-{datetime.now().year} Python Software Foundation')
    outputHandle('Scanning')
    outputHandle(f'\nCreating archive {os.path.join(modDir, f'{modName}.iwd')}\n')

    # function calls
    steps = [
        lambda arg1=modDir, arg2=modName, arg3=foldersToIgnore, arg4=filesToIgnore, arg5=outputHandle: buildIwd(arg1, arg2, arg3, arg4, arg5),
        lambda arg1=modName, arg2=modDir, arg3=activisionModDir, arg4=outputHandle: copyModIwdFromModToActivisionMod(arg1, arg2, arg3, arg4),
        lambda arg1=activisionModDir, arg2=modDir, arg3=outputHandle: copyModFfFromModToActivisionMod(arg1, arg2, arg3),
    ]

    # lambda's are anonymous functions, so we need to assign the function names manually
    # when not using lambda, the below '{step.__name__}' would work perfectly fine.
    steps[0].__name__ = 'build_iwd_step'
    steps[1].__name__ = 'copy_mod_iwd_step'
    steps[2].__name__ = 'copy_mod_ff_step'

    global stepFailure

    for step in steps:
        if stepFailure:
            break
        if processInterrupted:
            break
        try:
            step()
            if addSpaceBetweenSteps:
                outputHandle('\n'.strip())  # it adds 2 newlines w/o .strip()
        except Exception as error:
            stepFailure = True
            if onProgramFailureHandle:
                onProgramFailureHandle(f'Step {step.__name__} failed: {error}')
    
    if processInterrupted:
        if onProcessInterruptedHandle:
            onProcessInterruptedHandle('Process was interrupted by the user')
        return

    if not stepFailure:
        outputHandle('Everything is Ok')
        if onProgramSuccessHandle:
            onProgramSuccessHandle('Program finished with no errors')

def buildIwd(modDir: str, modName: str, foldersToIgnore: list, filesToIgnore: list, outputHandle=print) -> None:
    # Anything to be built into the modname.iwd will need its full mod dir path (exluding leading up to mod root).
    array = []

    itemsToPkgIntoIwd = grabModStructure(
        rootDir=modDir,
        foldersToIgnore=foldersToIgnore,
        filesToIgnore=filesToIgnore
    )

    iterateFiles(data=itemsToPkgIntoIwd, action=lambda x: array.append(x), outputHandle=outputHandle)

    iwdDest = os.path.join(modDir, f'{modName}.iwd')

    # delete old iwd if it exists
    if os.path.exists(iwdDest):
        os.remove(iwdDest)

    array = sorted(array)  # sort in ascending order

    # # Fake interruption (imitates user interruption)
    # i = 0
    # # Fake interruption (imitates user interruption)

    for item in array:
        # Add the file (item) to the zip archive
        with zipfile.ZipFile(iwdDest, 'a', zipfile.ZIP_DEFLATED) as zipf:  # 'a' for append, just be sure to delete old iwd first
            # Specify files and where you want them in the .iwd archive
            # For example, placing a specific file in the 'aitype' folder inside the iwd
            
            # Full path to the source file on the disk
            file_to_add = os.path.join(modDir, item).replace('\\', '/')
            # file_to_add = 'D:/SteamLibrary/steamapps/common/Call of Duty World at War/mods/zm_tst1/aitype/axis_zombie_ger_ber_sshonor.gsc'
            
            # Specify the destination path inside the iwd archive (as if you're recreating the folder structure)
            file_in_iwd = item
            # file_in_iwd = 'aitype/axis_zombie_ger_ber_sshonor.gsc'

            outputHandle(f'Compressing  {item}')
            
            # Add the file to the zip archive
            zipf.write(file_to_add, file_in_iwd)
        
        # # Fake interruption (imitates user interruption)
        # global processInterrupted
        # print(f'i: {i}')
        # i += 1
        # if i == 2:
        #     processInterrupted = True
        # # Fake interruption (imitates user interruption)

        if processInterrupted:
            break

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
def iterateFiles(data: dict, action: callable=None, outputHandle=print, parent: str='') -> None:
    for key, value in data.items():
        current_path = f'{parent}/{key}' if parent else key  # Join parent with current folder/file
        if isinstance(value, dict):  # If value is a dictionary, recurse
            iterateFiles(data=value, action=action, outputHandle=outputHandle, parent=current_path)
        else:  # If it's a file (None in this case), print the path
            if action:
                action(current_path)

def copyModIwdFromModToActivisionMod(modName: str, modDir: str, activisionModDir: str, outputHandle=print) -> None:
    modIwdSource = os.path.join(modDir, f'{modName}.iwd')
    modIwdDest = os.path.join(activisionModDir, f'{modName}.iwd')

    if not os.path.exists(activisionModDir):
        os.makedirs(activisionModDir)

    shutil.copy2(modIwdSource, modIwdDest)

    outputHandle(f'Copying  {modIwdSource}')
    outputHandle(f'     to  {modIwdDest}')

def copyModFfFromModToActivisionMod(activisionModDir: str, modDir: str, outputHandle=print) -> None:
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

            outputHandle(f'Copying  {modFfSource}')
            outputHandle(f'     to  {modFfDest}')
        else:
            outputHandle(f'Skipping copying  {modFfSource}')
            outputHandle(f'              to  {modFfDest}')
            outputHandle('          Reason  mod.ff already present')
    else:
        outputHandle(f'Skipping copying  {modFfSource}')
        outputHandle(f'              to  {modFfDest}')
        outputHandle('          Reason  mod.ff not present')

# Example usage
if __name__ == '__main__':
    # change these 2 as needed
    # NOTE: Be careful with variables that are in global scope like the below 2.
    #       I changed their styling from the args styling so functions couldn't access them unless passed as args.
    mod_name = 'zm_tst1'
    waw_root_dir = r'D:\SteamLibrary\steamapps\common\Call of Duty World at War'

    def outputHandleExample(message: str) -> None:
        print(message)
    
    def onProgramSuccessHandleExample(message: str) -> None:
        print(message)

    def onProgramFailureHandleExample(message: str) -> None:
        print(f'On program failure: {message}')
    
    def onProcessInterruptedHandleExample(message: str) -> None:
        print(f'On process interrupted: {message}')

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
        # outputHandle=outputHandleExample,  # uses print by default
        onProgramSuccessHandle=onProgramSuccessHandleExample,
        onProgramFailureHandle=onProgramFailureHandleExample,
        onProcessInterruptedHandle=onProcessInterruptedHandleExample,
        addSpaceBetweenSteps=True
    )
    print()  # to separate from vs output
