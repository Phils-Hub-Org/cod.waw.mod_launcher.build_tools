""" NOTE
    (1):
        When building sounds, it requires you to have a soundalias.csv file setup, i've provided a template file of which you just need to change the path.
        After the sound has successfully compiled, you can scrap the soundalias.csv file if you wish.
        p.s, Adding 'sound,custom_sound,,all_sp' to mod.csv section in the mod launcher is not required to build sounds, ..to play them in-game yes, but not build them.

        For more information refer to: 'misc/building-sounds-info.txt'

    (2):
        When testing, you will need to replace the below 'wawRootDir' with your actual WAW root directory.

    For console output refer to the screen_shots directory.
"""

import os, subprocess
from typing import Callable, Optional

stepFailure = False
processInterrupted = False

def build(
        binDir: str,
        buildOutputHandle=print,
        buildSuccessHandle: Optional[Callable]=None, buildFailureHandle: Optional[Callable]=None,
        buildInterruptedHandle: Optional[Callable]=None,
        addSpaceBetweenSteps=False) -> None:
    
    steps = [
        lambda arg1=binDir, arg2=buildOutputHandle: buildSounds(arg1, arg2),
    ]

    # lambda's are anonymous functions, so we need to assign the function names manually
    # when not using lambda, the below '{step.__name__}' would work perfectly fine.
    steps[0].__name__ = 'build_sounds_step'

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
        buildOutputHandle('Everything is Ok')
        if buildSuccessHandle:
            buildSuccessHandle('All steps completed successfully')

def buildSounds(binDir: str, buildOutputHandle=print) -> None:
    args = ['MODSound', '-pc', '-ignore_orphans']
    
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
            buildOutputHandle(output.strip())
    
        if processInterrupted:  # user interrupted
            process.kill()
            return

    # Capture the stderr output after the process finishes
    stderr = process.stderr.read()
    if stderr:
        buildOutputHandle(stderr.strip())

def interruptProcessHandle() -> None:
    global processInterrupted
    processInterrupted = True

# Example usage (below is an example of exactly how to utilize this module in your own script).
if __name__ == '__main__':
    # change these 2 as needed
    # NOTE: Be careful with variables that are in global scope like the below 2.
    #       I changed their styling from the args styling so functions couldn't access them unless passed as args.
    waw_root_dir = r'D:\SteamLibrary\steamapps\common\Call of Duty World at War' 
    bin_dir = os.path.join(waw_root_dir, 'bin')

    # Feel free to copy/paste these functions into your own script.
    def buildSoundOutputHandleSlot(message: str) -> None:
        print(f'Captured output: {message}')
    
    def buildSoundSuccessHandleSlot(message: str) -> None:
        print(f'On program success: {message}')

    def buildSoundFailureHandleSlot(message: str) -> None:
        print(f'On program failure: {message}')
    
    def buildSoundInterruptedHandleSlot(message: str) -> None:
        print(f'On process interrupted: {message}')
    
    # Imitates user interruption (just uncomment, adjust the delay and its good to go!).
    # import threading, time
    # threading.Thread(target=lambda: (time.sleep(0.1), interruptProcessHandle())).start()

    print()  # to separate from vs output
    build(
        ### These are all required args and dont need to be changed ###
        binDir=bin_dir,

        ### These are all optional args and can be changed ###
        # buildOutputHandle=buildSoundOutputHandleSlot,  # uses print by default
        buildSuccessHandle=buildSoundSuccessHandleSlot,
        buildFailureHandle=buildSoundFailureHandleSlot,
        buildInterruptedHandle=buildSoundInterruptedHandleSlot,
        addSpaceBetweenSteps=True
    )
    print()  # to separate from vs output
