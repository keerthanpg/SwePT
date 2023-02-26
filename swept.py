import argparse
import openai
import os
import requests

from git import Repo
from pathlib import Path
from typing import Union, Dict

ALLOWED_FILE_EXT = [".py"]
openai.api_key = openai.api_key = os.getenv('OPENAI_KEY', "")
gh_token = os.getenv('GH_TOKEN', "")


def get_edits_for_instruction(code: str, instruction: str) -> str:
  response = openai.Edit.create(
    model="code-davinci-edit-001",
    input=code,
    instruction=instruction,
  )
  code = response["choices"][0]["text"]
  return code


def edit_file(file: Union[str, Path], instruction: str) -> bool:
  if isinstance(file, str):
    file = Path(file)
  with open(file) as fob:
    file_contents = fob.read()
  is_modified = False
  modified_code = get_edits_for_instruction(file_contents, instruction)

  if modified_code != file_contents:  # any more checks?
    with open(file, "w") as fob:
      fob.write(modified_code)
      is_modified = True
  else:
    print("The code was not modified!")
  return is_modified


def display_diff(repo: Repo, file: Path) -> None:
  print(repo.git.diff([str(file)]))


def get_meta_info(instruction: str) -> Dict[str, str]:
  res = {
    "branch": "edit-code-example-1",
    "commit_message": "add edit",
    "pr_title": "Edit Code based on instruction",
    "pr_body": f"Edit the file based on the following instruction:\n{instruction}"
  }
  return res


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Edit a section of code, PR with changes.')
  parser.add_argument('-f', '--file', help='location of a file', required=True)
  parser.add_argument('-i', '--instruction', help='instruction on how to edit the file', type=str, required=True)
  parser.add_argument('-r', '--repo', help='location to git repo', type=str, default='./')
  parser.add_argument('-d', '--diff', help='show diff', action='store_true')
  parser.add_argument('-pr', '--pull-request', help='add change, commit, push and raise a PR', action='store_true')
  args = parser.parse_args()

  file = Path(args.file)
  repo_loc = Path(args.repo)
  instruction = args.instruction.strip()
  repo = Repo(repo_loc)

  assert file.exists() and file.is_file(), "File does not exist!"
  assert file.suffix in ALLOWED_FILE_EXT, "Filetype not supported"
  assert len(instruction) > 0, "Instruction not valid"
  assert not repo.bare, "Repo is bare!"

  is_modified = edit_file(file, instruction)

  if args.diff and is_modified:
    display_diff(repo, file)

  if args.pull_request and is_modified:
    meta = get_meta_info(instruction)
    current_branch = repo.active_branch.name
    print(f"0. Creating new-branch: {meta['branch']} (current-branch: {current_branch})")
    repo.git.checkout("-b", meta['branch'])

    print(f"1. Adding file: {file}")
    repo.git.add(str(file))

    print(f"2. Committing changes with message: {meta['commit_message']}")
    commit_output = repo.git.commit(m=meta['commit_message'])

    print("3. Push changes to remote (GitHub)")
    push_output = repo.git.push('--set-upstream', repo.remote().name, meta['branch'])

    print("4. Create a PR on GitHub")
    if gh_token == "":
      print("No GitHub token provided, cannot raise PR!")
    else:
      remote_url = repo.remotes.origin.url.replace(":", "/").replace(".git", "")
      repo_owner = remote_url.split("/")[-2]
      repo_name = remote_url.split("/")[-1]
      response = requests.post(
        url=f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls",
        data={
          "title": meta['pr_title'],
          "body": meta['pr_body'],
          "head": meta['branch'],
          "base": current_branch
        },
        headers={
          "Accept": "application/vnd.github+json",
          "Authorization": f"Bearer {gh_token}",
          "X-GitHub-Api-Version": "2022-11-28"
        }
      )

      print(response.json)

    print("5. Checking out current-branch, deleting local new-branch")
    repo.git.checkout(current_branch)
    repo.git.branch("-D", meta['branch'])
