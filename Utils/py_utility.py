import os, sys, subprocess
from win32com.client import Dispatch

def printProjectStructure(root_dir: str=os.getcwd(), files_to_ignore: list=[], folders_to_ignore: list=[], indent: int=0) -> None:
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        if os.path.isdir(item_path):
            if any(folder in item for folder in folders_to_ignore):
                continue
            print("  " * indent + f"📁 {item}")
            printProjectStructure(item_path, files_to_ignore, folders_to_ignore, indent + 1)
        else:
            if any(file_name in item for file_name in files_to_ignore):
                continue
            print("  " * indent + f"📄 {item}")

def isExecutable() -> bool:
    return getattr(sys, 'frozen', False)

def getTempUnpackPath() -> str:
    # When running as an executable, PyInstaller unpacks embedded files into a temporary directory
    unpack_path = os.path.join(sys._MEIPASS)

    return unpack_path

def createShortcut(target: str, shortcut_dest: str, icon_path: str = None, args: str = None, start_in: str = None) -> None:
    """Create a shortcut to a target file with optional arguments and start-in path."""
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_dest)
    shortcut.TargetPath = target
    if args:
        shortcut.Arguments = args
    if icon_path:
        shortcut.IconLocation = icon_path
    if start_in:
        shortcut.WorkingDirectory = start_in  # Set the "Start In" directory
    shortcut.save()

def runExecutable(running_dir, exe_path, exe_args) -> None:
    """
    Runs the given executable with no arguments.
    exe_path: Path to the executable file
    """

    os.chdir(running_dir)

    try:
        subprocess.Popen(
            [exe_path, exe_args],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        print(f"Successfully ran {exe_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {exe_path}: {e}")
    except FileNotFoundError:
        print(f"Executable not found: {exe_path}")

if __name__ == "__main__":
    printProjectStructure(
        files_to_ignore=[
            '.gitattributes',
            'LICENSE',
            'README.md'
        ],
        folders_to_ignore=[
            '.git',
            '.vscode',
            'output',
            '__pycache_',
            '--archived',
            '--misc',
            'Phils-Hub',
            'Tests'
        ]
    )