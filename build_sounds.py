""" NOTE
(1):
    When building sounds, it requires you to have a soundalias.csv file setup, i've provided a template file of which you just need to change the path.
    After the sound has successfully compiled, you can scrap the soundalias.csv file if you wish.
    p.s, Adding 'sound,custom_sound,,all_sp' to mod.csv section in the mod launcher is not required to build sounds, ..to play them in-game yes, but not build them.

    For more information refer to: 'Misc/building-sounds-info.txt'

(2):
    When testing, you will need to replace the below 'wawRootDir' with your actual WAW root directory.

For output information refer to: 'Misc/building-sounds-info.txt'
"""

import os, sys, subprocess

def build(binDir: str, printFunc=print) -> None:
    # function calls
    steps = [
        lambda arg1=binDir, arg2=printFunc: buildSounds(arg1, arg2),
    ]

    for step in steps:
        try:
            step()
        except Exception as error:
            teardown(f"Step {step.__name__} failed: {error}", printFunc)

def buildSounds(binDir: str, printFunc=print) -> None:
    args = ['MODSound', '-pc', '-ignore_orphans']
    # print(f'Args: {' '.join(args)}\n')
    
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
            printFunc(output.strip())

    # Capture the stderr output after the process finishes
    stderr = process.stderr.read()
    if stderr:
        printFunc(stderr.strip())

def teardown(message: str, printFunc=print) -> None:
    printFunc(message)
    sys.exit(1)

# Example usage
if __name__ == '__main__':
    # change these 2 as needed
    wawRootDir = r'D:\SteamLibrary\steamapps\common\Call of Duty World at War'
    binDir = os.path.join(wawRootDir, 'bin')

    print()  # to separate from vs output
    build(
        binDir=binDir,
        # printFunc=print  # the build func already utilizes print as the default output, so only use this arg when wanting to handle the output differently.
    )
    print()  # to separate from vs output