import sys
import time
import subprocess
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from collections import defaultdict

output_types = ["png", "jpg", "tiff", "svg"]
source_types = ["py", "pyde", "js", "html", "java"]

# Check for a .git folder, and "git init" if not
# git commit -m "First commit"

# Monitor changes to any of the output file types *and* any of the specified code
# file types, and if there are changes to *both* types of files, trigger a git add and git commit
# with an auto commit comment

# on startup enumerate all bare files in the directory and mark them as clean
# when they are changed, mark them as dirty
# when source files and image files are marked as dirty

file_list = defaultdict(str)

class ImageEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        fn_ext = event.src_path.lower().split(".")[-1]
        if event.event_type in ("created", "modified", "moved", "deleted") and (fn_ext in output_types or fn_ext in source_types):
            fn = event.src_path.split("/")[-1]
            if event.event_type == "moved":
                # copy the file's clean status to the new file name
                # and delete the old key
                new_fn = event.dest_path.split('/')[-1]
                file_list[new_fn] = file_list[fn]
                if fn in file_list:
                    del file_list[fn]
            #elif event.event_type == "deleted": # weird stuff happening here, maybe icloud drive related? saving creates delete event
            #    if fn in file_list:
            #        del file_list[fn]
            else:
                file_list[fn] = "dirty"
            
            # Check if both source files and output files have changed
            # (Changed some code and produced some image output)
            source_changed = any([file_list[x] == "dirty" for x in file_list if x.split(".")[-1] in source_types])
            output_changed = any([file_list[x] == "dirty" for x in file_list if x.split(".")[-1] in output_types])
            if source_changed and output_changed:
                add_and_commit("new source and output")
                # reset clean status for all files
                for fn in file_list:
                    file_list[fn] = "clean"
                

def discover_files():
    """
    Load up the current directory and add all code and image files.
    Mark all files 'clean' until they have been modified.
    """
    for fn in os.listdir("."):
        #fn_stripped = fn.split(".")[0]
        if fn.lower().split(".")[-1] in source_types:
            file_list[fn] = "clean"

def check_or_setup(src):
    """
    Check that the git command can execute successfully.
    Check for the presence of a .git folder in the project folder.
    Create a new repo if there is not one present, add, and do an initial commit.
    """
    if subprocess.call(["git", "--version"]) != 0:
        print("Error: git not found. Exiting.")
        sys.exit(1)
    if not os.path.exists(".git"):
        if subprocess.call(["git", "init"]) != 0:
            print("Error: failed to initialise repo. Exiting.")
            sys.exit(2)
    elif os.path.exists(".git") and not os.path.isdir(".git"):
        print("Error: .git exists but is not a directory. Exiting.")
        sys.exit(3)

def add_and_commit(msg):
    """
    Add all files and commit with the specified message.
    """
    subprocess.call(["git", "add", "."])
    subprocess.call(["git", "commit", "-m", msg])

if __name__ == "__main__":
    # os.getcwd()
    print(f"Starting in {os.getcwd()}")
    check_or_setup(".")
    discover_files()

    event_handler = ImageEventHandler()
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    add_and_commit("Session ended.")
