#!/usr/bin/env python
import json
from pathlib import Path
import os
import pathlib
import re
import shutil


ci_platform = "{{ cookiecutter.ci_platform }}"
license = "{{ cookiecutter.license }}"


def remove_path(path):
    p = pathlib.Path(path).resolve()
    if p.exists():
        if p.is_dir():
            shutil.rmtree(p)
        else:
            p.unlink()


def rename_file(path, new_name):
    p = pathlib.Path(path).resolve()
    p.rename(new_name)


def change_text(path, value, replacement):
    p = pathlib.Path(path).resolve()
    text = p.read_text()
    if isinstance(value, re.Pattern):
        text = value.sub(replacement, text)
    else:
        text = text.replace(value, replacement)
    p.write_text(text)


def change_files():
    if ci_platform != "GitLab":
        remove_path(".gitlab-ci.yml")
        remove_path("CONTRIBUTING.gitlab.md")
        rename_file("CONTRIBUTING.github.md", "CONTRIBUTING.md")
    if ci_platform != "Github":
        remove_path(".github")
        remove_path(".pre-commit-config.yml")
        remove_path("CODE_OF_CONDUCT.md")
        remove_path("CONTRIBUTING.github.md")
        rename_file("CONTRIBUTING.gitlab.md", "CONTRIBUTING.md")
    if license == "None":
        remove_path("LICENSE")
        change_text(
            "CONTRIBUTING.md",
            re.compile("This project is open-source under the [.*?license]"),
            "This project",
        )


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
    change_files()
