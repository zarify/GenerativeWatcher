# Generative Watcher
## About

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
(Watchdog)[https://pythonhosted.org/watchdog/index.html]

## Notes
- Some preliminary testing has been done with macOS 11 (Big Sur) using Python 3.8.6
- No doubt there are still some dumb bugs :)
- XCode command line tools need to be installed to install Watchdog via pip