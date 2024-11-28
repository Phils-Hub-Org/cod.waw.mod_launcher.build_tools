r""" WHEN mod.ff is present in AppData
Actual Outut:
    7-Zip (A) 4.42  Copyright (c) 1999-2006 Igor Pavlov  2006-05-14
    Copying  D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\zm_tst1.iwd
        to  C:\Users\Phil-\AppData\Local\Activision\CodWaW\mods\zm_tst1\zm_tst1.iwd
    Scanning

    Creating archive D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\zm_tst1.iwd

    Compressing  mod.csv

    Everything is Ok

Although the order is a bit janky imo, so ill ensure that the output is correct.
My Output:
    7-Zip (A) 4.42  Copyright (c) 1999-2006 Igor Pavlov  2006-05-14
    Scanning

    Creating archive D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\zm_tst1.iwd

    Compressing  mod.csv

    Copying  D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\zm_tst1.iwd
         to  C:\Users\Phil-\AppData\Local\Activision\CodWaW\mods\zm_tst1\zm_tst1.iwd

    Everything is Ok
"""

r""" WHEN mod.ff is NOT present in AppData
7-Zip (A) 4.42  Copyright (c) 1999-2006 Igor Pavlov  2006-05-14
Scanning
Copying  D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\mod.ff
     to  C:\Users\Phil-\AppData\Local\Activision\CodWaW\mods\zm_tst1\mod.ff
Copying  D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\zm_tst1.iwd
     to  C:\Users\Phil-\AppData\Local\Activision\CodWaW\mods\zm_tst1\zm_tst1.iwd

Creating archive D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\zm_tst1.iwd

Compressing  mod.csv

Everything is Ok
"""

import os, sys
# required for importing my custom modules
# only when trying to import from a '__main__' file that isn't run from root.
projRoot = os.getcwd()
if not projRoot in sys.path:
    sys.path.insert(0, projRoot)

from Tests.grabbingModIwdSelections import grabModStructure, iterateFiles

# NOTE: mod.ff only gets copied from mods > appdata if its not present in appdata.
# The actual compiling of the mod.ff file is obv not done here.

import os, subprocess, shutil, zipfile

WAW_ROOT_DIR = r'D:\SteamLibrary\steamapps\common\Call of Duty World at War'
MODS_DIR = os.path.join(WAW_ROOT_DIR, 'mods')
MOD_NAME = 'zm_tst1'
MOD_DIR = os.path.join(MODS_DIR, MOD_NAME)

homeDir = os.path.expanduser('~')
appdataDir = os.path.join(homeDir, 'AppData')
activisionDir = os.path.join(appdataDir, 'Local', 'Activision')
activisionModsDir = os.path.join(activisionDir, 'CoDWaW', 'mods')
ACTIVISION_MOD_DIR = os.path.join(activisionModsDir, MOD_NAME)

wawBin = os.path.join(WAW_ROOT_DIR, 'bin')

import subprocess
import os

def buildIwd():
    logList = []

    # print(f'\nBuild iwd start')
    # print(f"############################## ---/--/--- ##############################\n")
    
    # Anything to be built into the modname.iwd will need its full mod dir path (exluding leading up to mod root).
    # array = []

    # itemsToPkgIntoIwd = grabModStructure(
    #     root_dir=MOD_DIR,
    #     files_to_ignore=[
    #         'mod.ff',
    #         'zm_tst1.files',
    #         f'{MOD_NAME}.iwd',
    #     ],
    #     folders_to_ignore=[
    #         'sound',
    #     ]
    # )

    # iterateFiles(itemsToPkgIntoIwd, action=lambda x: array.append(x))

    iwdDest = os.path.join(MOD_DIR, f'{MOD_NAME}.iwd')

    # delete old iwd if it exists
    if os.path.exists(iwdDest):
        os.remove(iwdDest)

    array = [
        'mod.csv',
        'maps/createart/nazi_zombie_prototype_art.gsc',
        'maps/createfx/nazi_zombie_prototype_fx.gsc',
        'maps/nazi_zombie_prototype.gsc',
        'maps/nazi_zombie_prototype_fx.gsc',
    ]

    array = sorted(array)  # sort in ascending order

    for item in array:        
        with zipfile.ZipFile(iwdDest, 'a', zipfile.ZIP_DEFLATED) as zipf:  # 'a' for append, just be sure to delete old iwd first
            # Specify files and where you want them in the .iwd archive
            # For example, placing a specific file in the 'aitype' folder inside the iwd
            
            # Full path to the source file on the disk
            file_to_add = os.path.join(MOD_DIR, item).replace('\\', '/')
            # print(f"file_to_add: {file_to_add}")
            # file_to_add = 'D:/SteamLibrary/steamapps/common/Call of Duty World at War/mods/zm_tst1/aitype/axis_zombie_ger_ber_sshonor.gsc'
            
            # Specify the destination path inside the iwd archive (as if you're recreating the folder structure)
            file_in_iwd = item
            # file_in_iwd = 'aitype/axis_zombie_ger_ber_sshonor.gsc'
            # print(f"file_in_iwd: {file_in_iwd}")

            print(f'Compressing  {item}')
            
            # Add the file to the zip archive
            zipf.write(file_to_add, file_in_iwd)

        # # where to create the .iwd
        # iwdDest = os.path.join(MOD_DIR, f'{MOD_NAME}.iwd')
        # print(f'iwdDest  {iwdDest}')
        # if os.path.exists(iwdDest):
        #     # delete
        #     os.remove(iwdDest)

        # # # what to build into the .iwd
        # # 7za automatically adds 'aitype' folder and places the file in it? idk y
        # iwdSource = 'D:/SteamLibrary/steamapps/common/Call of Duty World at War/mods/zm_tst1/axis_zombie_ger_ber_sshonor.gsc'
        # # 7za does not add the aitype when explicitly specifying it, idk y
        # iwdSource = 'D:/SteamLibrary/steamapps/common/Call of Duty World at War/mods/zm_tst1/aitype/axis_zombie_ger_ber_sshonor.gsc'

        # args = ['7za', 'a', '-tzip', '-r', iwdDest, iwdSource]

        # # Use Popen to run the linker asynchronously
        # process = subprocess.Popen(
        #     args,
        #     cwd=wawBin,
        #     shell=True,
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.PIPE,
        #     text=True  # Enable text mode for easier string handling
        # )

        # # Read stdout and stderr in real time
        # while True:
        #     output = process.stdout.readline()
        #     if output == '' and process.poll() is not None:
        #         break
        #     if output:
        #         print(f'INFO: {output.strip()}')
        #         # logList.append(f'INFO: {output.strip()}')

        # # Capture the stderr output after the process finishes
        # stderr = process.stderr.read()
        # if stderr:
        #     print(f'ERROR: {stderr.strip()}')
        #     # logList.append(f'ERROR: {stderr.strip()}')

    with open('iwd.log', 'w') as f:
        for log in logList:
            f.write("%s\n" % log)

    # print(f'\n############################## ---/--/--- ##############################')
    # print(f'Build iwd end\n')

def copyModFfFromModToActivisionMod():
    # print(f'\nCopy mod.ff start')
    # print(f"############################## ---/--/--- ##############################\n")
    
    modFfSource = os.path.join(MOD_DIR, 'mod.ff')
    modFfDest = os.path.join(ACTIVISION_MOD_DIR, 'mod.ff')

    shutil.copy2(modFfSource, modFfDest)

    print(f"Copying  {modFfSource}")
    print(f"     to  {modFfDest}")

    # print(f'\n############################## ---/--/--- ##############################')
    # print(f'Copy mod.ff end\n')

def copyModIwdFromModToActivisionMod():
    # print(f'\nCopy mod.iwd start')
    # print(f"############################## ---/--/--- ##############################\n")
    
    modIwdSource = os.path.join(MOD_DIR, 'zm_tst1.iwd')
    modIwdDest = os.path.join(ACTIVISION_MOD_DIR, 'zm_tst1.iwd')

    shutil.copy2(modIwdSource, modIwdDest)

    print(f"Copying  {modIwdSource}")
    print(f"     to  {modIwdDest}")

    # print(f'\n############################## ---/--/--- ##############################')
    # print(f'Copy mod.iwd end\n')

if __name__ == "__main__":
    CLEAN = True
    # print()  # adds a newline

    try:
        print()  # to separate from vs output

        print('7-Zip (A) 4.42  Copyright (c) 1999-2006 Igor Pavlov  2006-05-14')
        print('Scanning')
        if CLEAN:
            print()
        print(f'Creating archive  {os.path.join(MOD_DIR, 'zm_tst1.iwd')}')
        
        if CLEAN:
            print()
        buildIwd()
        if CLEAN:
            print()
        if not os.path.exists(os.path.join(ACTIVISION_MOD_DIR, f'{MOD_NAME}.ff')):
            copyModFfFromModToActivisionMod()
        if CLEAN:
            print()
        copyModIwdFromModToActivisionMod()
        if CLEAN:
            print()
        print('Everything is Ok')

        print()  # to separate from vs output
    except Exception as e:
        print(e)
