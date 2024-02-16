#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2024 Red Hat, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import sys
import requests
from typing import Optional, List


def print_api_error(status_code: int) -> None:
    errors = {
        400: "Bad Request",
        401: "Session required",
        403: "Unauthorized access",
        404: "Not found"
    }
    if status_code not in errors.keys():
        print("Unknown API error")
    else:
        print(errors[status_code])


def load_readme(dir: str) -> Optional[str]:
    if not os.path.exists(readme_path):
        print(f"Invalid path: {readme_path} does not exist")
        return None
    with open(readme_path) as readme:
        readme_as_list = readme.readlines()
        escape_code_block(readme_as_list)
        readme_as_list.append("\n<br>\n")
        return "".join(readme_as_list)


def escape_code_block(lines: List[str]) -> None:
    """
    Ensures that all markdown code blocks created by backticks (```) are correctly
    closed, so that any lines added afterwards will be outside of a code block.
    Unclosed code blocks can occur after shortening readme.
    """
    backtick_count = 0
    for line in lines:
        if "```" in line:
            backtick_count += 1
    if backtick_count % 2 == 1:
        lines.append("...\n```")


def update_description(readme: str) -> bool:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {
        "description": readme
    }
    r = requests.put(API_REQUEST_PATH, headers=headers, json=data)
    if r.status_code != 200:
        print_api_error(r.status_code)
        return False
    return True


if __name__ == "__main__":
    token = os.environ["QUAY_API_TOKEN"]
    image_name = os.environ["IMAGE_NAME"]
    registry_namespace = os.environ["REGISTRY_NAMESPACE"]
    readme_path = os.environ["README_PATH"]

    API_REQUEST_PATH = f"https://quay.io/api/v1/repository/{registry_namespace}/{image_name}"

    readme = load_readme(readme_path)
    if readme is None:
        sys.exit(1)

    if not update_description(readme):
        sys.exit(1)
    print("Operation successful")
