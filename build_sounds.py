""" NOTE
(1):
    When building sounds, it requires you to have a soundalias.csv file setup, i've provided a template file of which you just need to change the path.
    After the sound has successfully compiled, you can scrap the soundalias.csv file if you wish.
    p.s, Adding 'sound,custom_sound,,all_sp' to mod.csv section in the mod launcher is not required to build sounds, ..to play them in-game yes, but not build them.

    For more information refer to: 'Misc/building-sounds-info.txt'

(2):
    When testing, you will need to replace the below 'wawRootDir' with your actual WAW root directory.

For console output refer to: 'Misc/building-sounds-info.txt'
"""

import os, subprocess

stepFailure = False
processInterrupted = False

def build(
        binDir: str,
        outputHandle=print,
        onProgramSuccessHandle=None, onProgramFailureHandle=None,
        onProcessInterruptedHandle=None,
        addSpaceBetweenSteps=False
    ) -> None:
    
    steps = [
        lambda arg1=binDir, arg2=outputHandle: buildSounds(arg1, arg2),
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
        if onProgramSuccessHandle:
            onProgramSuccessHandle('Everything is Ok')

def buildSounds(binDir: str, outputHandle=print) -> None:
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
            outputHandle(output.strip())
    
        if processInterrupted:  # user interrupted
            process.kill()
            return

    # Capture the stderr output after the process finishes
    stderr = process.stderr.read()
    if stderr:
        outputHandle(stderr.strip())

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
    def outputHandleExample(message: str) -> None:
        print(message)
    
    def onProgramSuccessHandleExample(message: str) -> None:
        print(f'On program success: {message}')

    def onProgramFailureHandleExample(message: str) -> None:
        print(f'On program failure: {message}')
    
    def onProcessInterruptedHandleExample(message: str) -> None:
        print(f'On process interrupted: {message}')
    
    # Imitates user interruption
    # import threading, time
    # threading.Thread(target=lambda: (time.sleep(0.1), interruptProcessHandle())).start()

    print()  # to separate from vs output
    build(
        binDir=bin_dir,
        # outputHandle=outputHandleExample,  # uses print by default
        onProgramSuccessHandle=onProgramSuccessHandleExample,
        onProgramFailureHandle=onProgramFailureHandleExample,
        onProcessInterruptedHandle=onProcessInterruptedHandleExample,
        addSpaceBetweenSteps=True
    )
    print()  # to separate from vs output
