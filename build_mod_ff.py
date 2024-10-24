r""" OUTPUT
# shutil
Copying  D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\mod.csv
     to  D:\SteamLibrary\steamapps\common\Call of Duty World at War\zone_source\mod.csv

subprocess
args: -nopause -language english -moddir zm_tst1 mod
Fastfile 1 of 1, "mod": [ver. 387] process...link...compress...save...done.

# shutil
Moving   D:\SteamLibrary\steamapps\common\Call of Duty World at War\zone\english\mod.ff
    to   D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\mod.ff
Copying  D:\SteamLibrary\steamapps\common\Call of Duty World at War\mods\zm_tst1\mod.ff
     to  C:\Users\Phil-\AppData\Local\Activision\CodWaW\mods\zm_tst1\mod.ff
"""

# NOTE:
    # When using this in a GUI application, you will need to grab the text from your mod.csv widget section and paste it into the mod.csv file before copying it from mods > zone_source.
    # I've added the logic to copy content from mod.csv in mod folder to zone_source folder. So all you need to do for a GUI-based application is copy text from mod.csv widget-section to mod.csv file in mod folder then this module can take care of the rest.

import os, subprocess, shutil

# uppercase used in funcs too, lowercase are not

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

    print(f"Moving  {os.path.join(MOD_DIR, 'mod.ff')}")
    print(f"    to  {os.path.join(ZONE_ENGLISH_DIR, 'mod.ff')}")

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

if __name__ == "__main__":
    CLEAN = True
    # print()  # adds a newline

    try:
        print()  # to separate from vs output

        copyModCsvFromModToZoneSource()
        if CLEAN:
            print()
        buildModFf()
        if CLEAN:
            print()
        moveModFfFromZoneEnglishToMod()
        if CLEAN:
            print()
        copyModFfFromModToActivisionMod()

        print()  # to separate from vs output
    except Exception as e:
        print(e)
