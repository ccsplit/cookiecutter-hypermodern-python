#!/usr/bin/env python
import json
from pathlib import Path
import os
import pathlib
import shutil


ci_platform = "{{ cookiecutter.ci_platform }}"
print(ci_platform)


def remove_path(path):
    cur_dir = pathlib.Path(os.getcwd())
    p = cur_dir.joinpath(path).resolve()
    if p.exists():
        if p.is_dir():
            shutil.rmtree(p)
        else:
            p.unlink()


def remove_ci():
    if ci_platform != "GitLab":
        remove_path(".gitlab-ci.yml")
    if ci_platform != "Github":
        remove_path(".gitlab")


def reindent_cookiecutter_json():
    """Indent .cookiecutter.json using two spaces.

    The jsonify extension distributed with Cookiecutter uses an indentation
    width of four spaces. This conflicts with the default indentation width of
    Prettier for JSON files. Prettier is run as a pre-commit hook in CI.
    """
    path = Path(".cookiecutter.json")

    with path.open() as io:
        data = json.load(io)

    with path.open(mode="w") as io:
        json.dump(data, io, sort_keys=True, indent=2)
        io.write("\n")


if __name__ == "__main__":
    reindent_cookiecutter_json()
    remove_ci()
