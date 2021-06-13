# Generative Watcher

A little tool for keeping track of what script config generated what output.
When run in a directory containing any of the specified source file types (defaults to .py, .pyde, .js, .java, .html)
it watches for creation or modification of one of the specified output file types (defaults to .png, .jpg, .tiff, .svg)
and when at least one of each type of file as changed runs a git add and commit, saving a copy into the repo.
This allows a tool like the GitHub Desktop app to browse through the commit history, preview images which have been added
and show diffs in any code committed.

## Usage
Just run the script from the command line from whatever folder you're working in:
```bash
python /path/to/watch_diff.py
```
- If no git repository is found a new one will be created
- Script will exit if .git is found but not a directory, git is not present in your path, or if git init fails
- An automatic add/commit is triggered when a source and an output file have been modified or created
- Exit with Ctrl-C and an add/commit will be triggered to end the session
## Dependencies
Watchdog - https://pythonhosted.org/watchdog/index.html

## Notes
- Some preliminary testing has been done with macOS 11 (Big Sur) using Python 3.8.6
- No doubt there are still some dumb bugs :)
- XCode command line tools need to be installed to install Watchdog via pip
- **Seems to be broken in a few horrible ways where the image doesn't get put into the git repo properly :(**

# Click Save
A better way to selectively save different versions of Processing code, although it doesn't solve the code version issue which Generative Watcher was designed to address.

## Usage
Designed for static sketches (i.e. noLoop()).

Put a noLoop() call at the end of draw().

```python
from click_save import *

...setup code etc...

def draw():

    ...other draw code...

    noLoop()
```

The click code is just:

```python
import datetime

def mouseClicked(event):
    if event.button == 37: # left
        print("Next.")
        loop()
    elif event.button == 39: # right
        stamp = datetime.datetime.now().replace(microsecond=0).isoformat()
        stamp = stamp.replace(":","-")
        fn = "versions/" + stamp + ".png"
        save(fn)
        print("Saved.")
```

Left click simply generates a new version of the draw code by turning looping on again (which then gets stopped at the end of the draw function), whilst right-click saves a copy of the output with a timestamp.

## Notes
This assumes that all relevant generation code is sitting in your draw function, so when draw is run again you get a whole new copy of your output.