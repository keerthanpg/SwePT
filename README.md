# SwePT
AI sends pull requests for features you request in natural language


## Usage
```
python swept.py -h                                                                                              
usage: swept.py [-h] -f FILE -i INSTRUCTION [-r REPO] [-d] [-pr]

Edit a section of code, PR with changes.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  location of a file
  -i INSTRUCTION, --instruction INSTRUCTION
                        instruction on how to edit the file
  -r REPO, --repo REPO  location to git repo
  -d, --diff            show diff
  -pr, --pull-request   add change, commit, push and raise a PR

```

## Example
```
OPENAI_KEY="<key>" GH_TOKEN="<token>" python swept.py -f examples/import_indent_bug.py -i "Rewrite the given code and fix any bugs in the program." -d --pr
```
Here is a real PR opened by this above command: https://github.com/keerthanpg/SwePT/pull/8