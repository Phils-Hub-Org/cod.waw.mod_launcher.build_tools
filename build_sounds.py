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

import os, subprocess

# uppercase used in funcs too, lowercase are not

wawRootDir = r'D:\SteamLibrary\steamapps\common\Call of Duty World at War'
WAW_BIN_DIR = os.path.join(wawRootDir, 'bin')

def buildSounds():
    # print(f"\nBuild sounds start")
    # print(f"############################## ---/--/--- ##############################\n")

    args = ['MODSound', '-pc', '-ignore_orphans']
    # print(f'Args: {' '.join(args)}\n')
    
    # Use Popen to run the linker asynchronously
    process = subprocess.Popen(
        args,
        cwd=WAW_BIN_DIR,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True  # Enable text mode for easier string handling
    )
    
    # Read stdout and stderr
    stdout, stderr = process.communicate()

    # Process and print stdout lines
    for line in stdout.splitlines():
        # print(f"INFO: {line}")
        print(line)

    # Process and print stderr lines
    for line in stderr.splitlines():
        # print(f"ERROR: {line}")
        print(line)

    # print(f"\n############################## ---/--/--- ##############################")
    # print(f"Build sounds end\n")

if __name__ == '__main__':
    try:
        buildSounds()
    except Exception as e:
        print(e)
