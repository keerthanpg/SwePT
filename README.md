# Japeeti
AI sends pull requests for features you request in natural language

- Create frontend website for marketing 
- Semantic search for what files to update and recursive update
- Slackbot that takes requests from users and responds with PR links
- Github api to retrieve PR comments and what file, line num it correspond to 


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


```
OPENAI_KEY="<key>" GH_TOKEN="<token>" python swept.py
-f /Users/keerthanapg/robotics_transformer/tokenizers/image_tokenizer.py -i "Rewrite the given code by making the __call__ function always use token learner and remove use_token_learner and self._use_token_learner variable" -r "/Users/keerthanapg/robotics_transformer" -d -pr
```
Here is a more complex PR opened on an open source repo: https://github.com/keerthanpg/robotics_transformer/pull/5/commits/20dda2730774a414cfd6a59e59f8870c83ce6307