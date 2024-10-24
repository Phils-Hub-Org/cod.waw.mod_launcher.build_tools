""" SUCCESS
---------------------------
        Errors
---------------------------


---------------------------
FILES:          18315
UPDATED:        6
ERRORS:         20570
----------------------------
"""

""" FAILURE
---------------------------
        Errors
---------------------------


---------------------------
FILES:          18315
UPDATED:        4
ERRORS:         20570
----------------------------
"""

""" NOTE
(1):
    When building sounds, it requires you to have a soundalias.csv file setup, i've provided a template file of which you just need to change the path.
    After the sound has successfully compiled, you can scrap the soundalias.csv file if you wish.
    p.s, Adding 'sound,custom_sound,,all_sp' to mod.csv section in the mod launcher is not required to build sounds, play them in-game yes, but not build them.

    For more information refer to: 'Misc/building-sounds-info.txt'

(2):
    When testing, you will need to replace the below 'wawRootDir' with your actual WAW root directory.

Below vars:
    UPPERCASE: Used globally (scope: module) and locally (scope: function)
    lowercase: used globally (scope: module)
"""

import os, subprocess

wawRootDir = r'D:\SteamLibrary\steamapps\common\Call of Duty World at War'
BIN_DIR = os.path.join(wawRootDir, 'bin')

def buildSounds():
    # print(f"\nBuild sounds start")
    # print(f"############################## ---/--/--- ##############################\n")

    args = ['MODSound', '-pc', '-ignore_orphans']
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

    # print(f"\n############################## ---/--/--- ##############################")
    # print(f"Build sounds end\n")

if __name__ == '__main__':
    try:
        buildSounds()
    except Exception as e:
        print(e)
