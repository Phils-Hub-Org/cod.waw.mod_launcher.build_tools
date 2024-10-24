r""" STOCK MOD LAUNCHER OUTPUT
WHEN modName.iwd is present in AppData
    Actual Outut (Although the order is fine, ill add some new lines to my version for clarity):
        Copying  D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\mod.csv
            to  D:\SteamLibrary\steamapps\common\Call of Duty World at War\zone_source\mod.csv
        args: -nopause -language english -moddir zm_tst1 mod
        Fastfile 1 of 1, "mod": [ver. 387] process...link...compress...save...done.
        Moving   D:\SteamLibrary\steamapps\common\Call of Duty World at War\zone\english\mod.ff
            to   D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\mod.ff
        Copying  D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\mod.ff
            to  C:\Users\Phil-\AppData\Local\Activision\CodWaW\mods\zm_tst1\mod.ff
    
    My Output:
        Copying  D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\mod.csv
            to  D:\SteamLibrary\steamapps\common\Call of Duty World at War\zone_source\mod.csv 

        args: -nopause -language english -moddir zm_tst1 mod
        Fastfile 1 of 1, "mod": [ver. 387] process...link...compress...save...done.

        Moving  D:\SteamLibrary\steamapps\common\Call of Duty World at War\zone\english\mod.ff 
            to  D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\mod.ff 

        Copying  D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\mod.ff
            to  C:\Users\Phil-\AppData\Local\Activision\CoDWaW\mods\zm_tst1\mod.ff

WHEN modName.iwd is NOT present in AppData
    Actual Outut: (Again, the order is fine, but ill add some new lines to my version for clarity):
        Copying  D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\mod.csv
            to  D:\SteamLibrary\steamapps\common\Call of Duty World at War\zone_source\mod.csv
        args: -nopause -language english -moddir zm_tst1 mod
        Fastfile 1 of 1, "mod": [ver. 387] process...link...compress...save...done.
        Moving   D:\SteamLibrary\steamapps\common\Call of Duty World at War\zone\english\mod.ff
            to   D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\mod.ff
        Copying  D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\mod.ff
            to  C:\Users\Phil-\AppData\Local\Activision\CodWaW\mods\zm_tst1\mod.ff
        Copying  D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\zm_tst1.iwd
            to  C:\Users\Phil-\AppData\Local\Activision\CodWaW\mods\zm_tst1\zm_tst1.iwd
    
    My Output:
        Copying  D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\mod.csv
            to  D:\SteamLibrary\steamapps\common\Call of Duty World at War\zone_source\mod.csv 

        args: -nopause -language english -moddir zm_tst1 mod
        Fastfile 1 of 1, "mod": [ver. 387] process...link...compress...save...done.

        Moving  D:\SteamLibrary\steamapps\common\Call of Duty World at War\zone\english\mod.ff      
            to  D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\mod.ff      

        Copying  D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\mod.ff     
            to  C:\Users\Phil-\AppData\Local\Activision\CoDWaW\mods\zm_tst1\mod.ff

        Copying  D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\zm_tst1.iwd
            to  C:\Users\Phil-\AppData\Local\Activision\CoDWaW\mods\zm_tst1\zm_tst1.iwd
"""

""" NOTE
(1):
    modName.iwd only gets copied to mods > appdata if its not present in the appdata/mods folder.
    The actual building of the modName.iwd file is obv not done here.

(2):
    When using this in a GUI application, you will need to grab the text from your mod.csv widget section and paste it into the mod.csv file before copying it from mods > zone_source.
    I've added the logic to copy content from mod.csv in mod folder to zone_source folder. So all you need to do for a GUI-based application is copy text from mod.csv widget-section to mod.csv file in mod folder then this module can take care of the rest.

(3):
    When testing, you will need to replace the below 'wawRootDir' with your actual WAW root directory
    as well as the 'MOD_NAME' with the actual name of your mod.

Below vars:
    UPPERCASE: Used globally (scope: module) and locally (scope: function)
    lowercase: used globally (scope: module)
"""

import os, subprocess, shutil

wawRootDir = r'D:\SteamLibrary\steamapps\common\Call of Duty World at War'
BIN_DIR = os.path.join(wawRootDir, 'bin')

MODS_DIR = os.path.join(wawRootDir, 'mods')
MOD_NAME = 'zm_tst1'
MOD_DIR = os.path.join(MODS_DIR, MOD_NAME)

ZONESOURCE_DIR = os.path.join(wawRootDir, 'zone_source')
ZONE_ENGLISH_DIR = os.path.join(wawRootDir, 'zone', 'english')

homeDir = os.path.expanduser('~')
appdataDir = os.path.join(homeDir, 'AppData')
activisionDir = os.path.join(appdataDir, 'Local', 'Activision')
activisionModsDir = os.path.join(activisionDir, 'CoDWaW', 'mods')
ACTIVISION_MOD_DIR = os.path.join(activisionModsDir, MOD_NAME)

def copyModCsvFromModToZoneSource():
    # print(f'\nBuild mod.csv start')
    # print(f"############################## ---/--/--- ##############################\n")

    shutil.copy2(os.path.join(MOD_DIR, 'mod.csv'), os.path.join(ZONESOURCE_DIR, 'mod.csv'))
    
    print(f"Copying  {os.path.join(MOD_DIR, 'mod.csv')}")
    print(f"     to  {os.path.join(ZONESOURCE_DIR, 'mod.csv')}")

    # print(f'\n############################## ---/--/--- ##############################')
    # print(f'Build mod.csv end\n')

def buildModFf():
    # print(f'\nBuild mod.ff start')
    # print(f"############################## ---/--/--- ##############################\n")
    
    args = ['linker_pc', '-nopause', '-language', 'english', '-moddir', MOD_NAME, 'mod']
    # print(f'Args: {' '.join(args)}\n')

    # Use Popen to run the linker asynchronously
    process = subprocess.Popen(
        args,
        cwd=BIN_DIR,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True  # Enable text mode for easier string handling
    )
    
    # Read stdout and stderr in real time
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            # print(f'INFO: {output.strip()}')
            print(output.strip())

    # Capture the stderr output after the process finishes
    stderr = process.stderr.read()
    if stderr:
        # print(f'ERROR: {stderr.strip()}')
        print(stderr.strip())

    # print(f'\n############################## ---/--/--- ##############################')
    # print(f'Build mod.ff end\n')

def moveModFfFromZoneEnglishToMod():
    # print(f'\nMove mod.ff start')
    # print(f"############################## ---/--/--- ##############################\n")
    
    modFfSource = os.path.join(ZONE_ENGLISH_DIR, 'mod.ff')
    modFfDest = os.path.join(MOD_DIR, 'mod.ff')

    shutil.move(modFfSource, modFfDest)

    print(f"Moving  {os.path.join(ZONE_ENGLISH_DIR, 'mod.ff')}")
    print(f"    to  {os.path.join(MOD_DIR, 'mod.ff')}")

    # print(f'\n############################## ---/--/--- ##############################')
    # print(f'Move mod.ff end\n')

def copyModFfFromModToActivisionMod():
    # print(f'\nCopy mod.ff start')
    # print(f"############################## ---/--/--- ##############################\n")
    
    modFfSource = os.path.join(MOD_DIR, 'mod.ff')
    modFfDest = os.path.join(ACTIVISION_MOD_DIR, 'mod.ff')

    if not os.path.exists(ACTIVISION_MOD_DIR):
        os.makedirs(ACTIVISION_MOD_DIR)

    shutil.copy2(modFfSource, modFfDest)

    print(f"Copying  {modFfSource}")
    print(f"     to  {modFfDest}")

    # print(f'\n############################## ---/--/--- ##############################')
    # print(f'Copy mod.ff end\n')

# Just a nice touch that the stock launcher has where it ensures the modName.iwd is present in appdata/mods folder during the mod.ff stage.
def copyIwdFromModToActivisionMod():
    # print(f'\nCopy modName.iwd start')
    # print(f"############################## ---/--/--- ##############################\n")
    
    # if modName.iwd is already present in appdata/mods, then return
    # Additional (handy, but not required) step to ensure the modName.iwd is present in appdata/mods folder.
    # As prev mentioned, this is default stock launcher behavior.
    if os.path.exists(os.path.join(ACTIVISION_MOD_DIR, f'{MOD_NAME}.iwd')):
        return

    modIwdSource = os.path.join(MOD_DIR, f'{MOD_NAME}.iwd')
    modIwdDest = os.path.join(ACTIVISION_MOD_DIR, f'{MOD_NAME}.iwd')

    if not os.path.exists(ACTIVISION_MOD_DIR):
        os.makedirs(ACTIVISION_MOD_DIR)

    shutil.copy2(modIwdSource, modIwdDest)

    print(f"Copying  {modIwdSource}")
    print(f"     to  {modIwdDest}")

    # print(f'\n############################## ---/--/--- ##############################')
    # print(f'Copy modName.iwd end\n')

if __name__ == "__main__":
    CLEAN = True  # print()  # adds a newline

    steps = [
        lambda: copyModCsvFromModToZoneSource(),
        lambda: buildModFf(),
        lambda: moveModFfFromZoneEnglishToMod(),
        lambda: copyModFfFromModToActivisionMod(),
        lambda: copyIwdFromModToActivisionMod()
    ]

    print()  # to separate from vs output

    try:
        for step in steps:
            if CLEAN:
                print()
            step()

    except Exception as error:
        print(error)
    
    print()  # to separate from vs output
