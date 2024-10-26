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
from typing import Callable, Optional

stepFailure = False
processInterrupted = False

def build(
        modName: str, modDir: str, activisionModDir: str,
        foldersToIgnore: list=[], filesToIgnore: list=[], extensionsToIgnore: list=[],
        buildOutputHandle=print,
        buildSuccessHandle: Optional[Callable]=None, buildFailureHandle: Optional[Callable]=None,
        buildInterruptedHandle: Optional[Callable]=None,
        addSpaceBetweenSteps=False) -> None:

    buildOutputHandle(f'Python zipfile (P) {platform.python_version()}')
    buildOutputHandle(f'Copyright (c) 2001-{datetime.now().year} Python Software Foundation')
    buildOutputHandle('Scanning')
    x = '\n' if addSpaceBetweenSteps else ''  # if newline, add above and below
    buildOutputHandle(f'{x}Creating archive {os.path.join(modDir, f'{modName}.iwd')}{x}')

    steps = [
        lambda arg1=modDir, arg2=modName, arg3=foldersToIgnore, arg4=filesToIgnore, arg5=extensionsToIgnore, arg6=buildOutputHandle: buildIwd(arg1, arg2, arg3, arg4, arg5, arg6),
        lambda arg1=modName, arg2=modDir, arg3=activisionModDir, arg4=buildOutputHandle: copyModIwdFromModToActivisionMod(arg1, arg2, arg3, arg4),
        lambda arg1=activisionModDir, arg2=modDir, arg3=buildOutputHandle: copyModFfFromModToActivisionMod(arg1, arg2, arg3),
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
                buildOutputHandle('\n'.strip())  # it adds 2 newlines w/o .strip()
        except Exception as error:
            stepFailure = True
            if buildFailureHandle:
                buildFailureHandle(f'Step {step.__name__} failed: {error}')
    
    if processInterrupted:
        if buildInterruptedHandle:
            buildInterruptedHandle('Process was interrupted by the user')
        return

    if not stepFailure:
        if buildSuccessHandle:
            buildSuccessHandle('Everything is Ok')

def buildIwd(modDir: str, modName: str, foldersToIgnore: list, filesToIgnore: list, extensionsToIgnore:list, buildOutputHandle=print) -> None:
    # Anything to be built into the modname.iwd will need its full mod dir path (exluding leading up to mod root).
    array = []

    itemsToPkgIntoIwd = grabModStructure(
        rootDir=modDir,
        foldersToIgnore=foldersToIgnore,
        filesToIgnore=filesToIgnore,
        extensionsToIgnore=extensionsToIgnore
    )

    iterateFiles(data=itemsToPkgIntoIwd, action=lambda x: array.append(x), buildOutputHandle=buildOutputHandle)

    iwdDest = os.path.join(modDir, f'{modName}.iwd')

    # delete old iwd if it exists
    if os.path.exists(iwdDest):
        os.remove(iwdDest)

    array = sorted(array)  # sort in ascending order

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

            buildOutputHandle(f'Compressing  {item}')
            
            # Add the file to the zip archive
            zipf.write(file_to_add, file_in_iwd)

        if processInterrupted:
            break

# Utilized by: buildIwd()
def grabModStructure(rootDir: str=os.getcwd(), foldersToIgnore: list=[], filesToIgnore: list=[], extensionsToIgnore: list=[]) -> dict:
    structure = {}
    for item in os.listdir(rootDir):
        item_path = os.path.join(rootDir, item)
        if os.path.isdir(item_path):
            if any(folder in item for folder in foldersToIgnore):
                continue
            # Recursively build the folder structure
            structure[item] = grabModStructure(item_path, foldersToIgnore, filesToIgnore, extensionsToIgnore)
        else:
            # Check for file names and extensions to ignore
            if any(fileName in item for fileName in filesToIgnore) or any(item.endswith(ext) for ext in extensionsToIgnore):
                continue
            # Store the file in the dictionary
            structure[item] = None
    return structure

# Utilized by: buildIwd()
def iterateFiles(data: dict, action: Callable=None, buildOutputHandle=print, parent: str='') -> None:
    for key, value in data.items():
        current_path = f'{parent}/{key}' if parent else key  # Join parent with current folder/file
        if isinstance(value, dict):  # If value is a dictionary, recurse
            iterateFiles(data=value, action=action, buildOutputHandle=buildOutputHandle, parent=current_path)
        else:  # If it's a file (None in this case), print the path
            if action:
                action(current_path)

def copyModIwdFromModToActivisionMod(modName: str, modDir: str, activisionModDir: str, buildOutputHandle=print) -> None:
    modIwdSource = os.path.join(modDir, f'{modName}.iwd')
    modIwdDest = os.path.join(activisionModDir, f'{modName}.iwd')

    if not os.path.exists(activisionModDir):
        os.makedirs(activisionModDir)

    shutil.copy2(modIwdSource, modIwdDest)

    buildOutputHandle(f'Copying  {modIwdSource}')
    buildOutputHandle(f'     to  {modIwdDest}')

def copyModFfFromModToActivisionMod(activisionModDir: str, modDir: str, buildOutputHandle=print) -> None:
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

            buildOutputHandle(f'Copying  {modFfSource}')
            buildOutputHandle(f'     to  {modFfDest}')
        else:
            buildOutputHandle(f'Skipping copying  {modFfSource}')
            buildOutputHandle(f'              to  {modFfDest}')
            buildOutputHandle('          Reason  mod.ff already present')
    else:
        buildOutputHandle(f'Skipping copying  {modFfSource}')
        buildOutputHandle(f'              to  {modFfDest}')
        buildOutputHandle('          Reason  mod.ff not present')

def interruptProcessHandle() -> None:
    global processInterrupted
    processInterrupted = True

# Example usage
if __name__ == '__main__':
    # change these 2 as needed
    # NOTE: Be careful with variables that are in global scope like the below 2.
    #       I changed their styling from the args styling so functions couldn't access them unless passed as args.
    mod_name = 'zm_tst1'
    waw_root_dir = r'D:\SteamLibrary\steamapps\common\Call of Duty World at War'

    # Feel free to copy/paste these functions into your own script.
    def buildIWDOutputHandleSlot(message: str) -> None:
        print(f'Captured output: {message}')
    
    def buildIWDSuccessHandleSlot(message: str) -> None:
        print(f'On program success: {message}')

    def buildIWDFailureHandleSlot(message: str) -> None:
        print(f'On program failure: {message}')
    
    def buildIWDInterruptedHandleSlot(message: str) -> None:
        print(f'On process interrupted: {message}')
    
    # Imitates user interruption (just uncomment, adjust the delay and its good to go!).
    # import threading, time
    # threading.Thread(target=lambda: (time.sleep(0.1), interruptProcessHandle())).start()

    print()  # to separate from vs output
    build(
        ### These are all required args and dont need to be changed ###
        modName=mod_name,
        modDir=os.path.join(waw_root_dir, 'mods', mod_name),
        activisionModDir=os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Activision', 'CoDWaW', 'mods', mod_name),  # '~' = home dir

        ### These are all optional args and can be changed ###
        foldersToIgnore=[
            'sound',
        ],
        filesToIgnore=[
            'how-to-notes.md',
            'screen-grab-of-map.png',
        ],
        extensionsToIgnore=[
            '.ff',
            '.iwd',
            '.log',
            '.txt',
            '.files',
        ],
        ### These are all optional args and can be changed ###
        # buildOutputHandle=buildIWDOutputHandleSlot,  # uses print by default
        buildSuccessHandle=buildIWDSuccessHandleSlot,
        buildFailureHandle=buildIWDFailureHandleSlot,
        buildInterruptedHandle=buildIWDInterruptedHandleSlot,
        addSpaceBetweenSteps=True
    )
    print()  # to separate from vs output
