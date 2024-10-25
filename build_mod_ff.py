""" NOTE
(1):
    When testing, you will need to replace the below 'wawRootDir' with your actual WAW root directory
    as well as the 'modName' with the actual name of your mod.

(2):
    The default stock mod launcher behaviour is to copy modName.iwd to appdata/mods folder if it is not present there.
    So this module does take care of that, but for the actual building of the .iwd, check out the 'build_iwd.py' module.

(3):
    When using this in a GUI application, you will need to grab the text from your mod.csv widget section and paste it into the mod.csv file before copying it from mods > zone_source.
    I've added the logic to copy content from mod.csv in mod folder to zone_source folder. So all you need to do for a GUI-based application is copy text from mod.csv widget-section to mod.csv file in mod folder then this module can take care of the rest.    
"""

import os, sys, subprocess, shutil

def copyModCsvFromModToZoneSource(modDir: str, zoneSourceDir: str) -> None:
    shutil.copy2(os.path.join(modDir, 'mod.csv'), os.path.join(zoneSourceDir, 'mod.csv'))
    
    print(f"Copying  {os.path.join(modDir, 'mod.csv')}")
    print(f"     to  {os.path.join(zoneSourceDir, 'mod.csv')}")

def buildModFf(modName: str, binDir: str) -> None:
    args = ['linker_pc', '-nopause', '-language', 'english', '-moddir', modName, 'mod']

    # Use Popen to run the linker asynchronously
    process = subprocess.Popen(
        args,
        cwd=binDir,
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
            print(output.strip())

    # Capture the stderr output after the process finishes
    stderr = process.stderr.read()
    if stderr:
        print(stderr.strip())

def moveModFfFromZoneEnglishToMod(zoneEnglishDir: str, modDir: str) -> None:
    modFfSource = os.path.join(zoneEnglishDir, 'mod.ff')
    modFfDest = os.path.join(modDir, 'mod.ff')

    shutil.move(modFfSource, modFfDest)

    print(f"Moving  {os.path.join(zoneEnglishDir, 'mod.ff')}")
    print(f"    to  {os.path.join(modDir, 'mod.ff')}")

def copyModFfFromModToActivisionMod(activisionModDir: str, modDir: str) -> None:
    if not os.path.exists(activisionModDir):
        os.makedirs(activisionModDir)

    modFfSource = os.path.join(modDir, 'mod.ff')
    modFfDest = os.path.join(activisionModDir, 'mod.ff')

    shutil.copy2(modFfSource, modFfDest)

    print(f"Copying  {modFfSource}")
    print(f"     to  {modFfDest}")

# Just a nice touch that the stock launcher has where it ensures the modName.iwd is present in appdata/mods folder during the mod.ff stage.
def copyIwdFromModToActivisionMod(activisionModDir: str, modDir: str, modName: str) -> None:
    if not os.path.exists(activisionModDir):
        os.makedirs(activisionModDir)

    modIwdSource = os.path.join(modDir, f'{modName}.iwd')
    modIwdDest = os.path.join(activisionModDir, f'{modName}.iwd')
    
    # step 1: check if present in root/mods
    if os.path.exists(modIwdSource):
        # print('iwd present in root/mods')

        # step 2: check if not present in appdata/mods
        if not os.path.exists(modIwdDest):
            # print('iwd not in appdata/mods')

            shutil.copy2(modIwdSource, modIwdDest)

    print(f"Copying  {modIwdSource}")
    print(f"     to  {modIwdDest}")

def teardown(message: str) -> None:
    print(message)
    sys.exit(1)

def buildMod(modDir: str, zoneSourceDir: str, modName: str, binDir: str, zoneEnglishDir: str, activisionModDir: str) -> None:
    CLEAN = True  # print()  # adds a newline

    # function calls
    steps = [
        lambda arg1=modDir, arg2=zoneSourceDir: copyModCsvFromModToZoneSource(arg1, arg2),
        lambda arg1=modName, arg2=binDir: buildModFf(arg1, arg2),
        lambda arg1=zoneEnglishDir, arg2=modDir: moveModFfFromZoneEnglishToMod(arg1, arg2),
        lambda arg1=activisionModDir, arg2=modDir: copyModFfFromModToActivisionMod(arg1, arg2),
        lambda arg1=activisionModDir, arg2=modDir, arg3=modName: copyIwdFromModToActivisionMod(arg1, arg2, arg3),
    ]

    for step in steps:
        try:
            if CLEAN:
                print()
            step()
        except Exception as error:
            teardown(f"Step {step.__name__} failed: {error}")

if __name__ == '__main__':
    # change these 2 as needed
    modName = 'zm_tst1'
    wawRootDir = r'D:\SteamLibrary\steamapps\common\Call of Duty World at War'

    # you can leave these alone
    binDir = os.path.join(wawRootDir, 'bin')
    modsDir = os.path.join(wawRootDir, 'mods')
    modDir = os.path.join(modsDir, modName)
    zoneSourceDir = os.path.join(wawRootDir, 'zone_source')
    zoneEnglishDir = os.path.join(wawRootDir, 'zone', 'english')
    activisionModDir = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Activision', 'CoDWaW', 'mods', modName)  # '~' = home dir

    print()  # to separate from vs output
    buildMod(
        modDir=modDir,
        zoneSourceDir=zoneSourceDir,
        modName=modName,
        binDir=binDir,
        zoneEnglishDir=zoneEnglishDir,
        activisionModDir=activisionModDir
    )
    print()  # to separate from vs output