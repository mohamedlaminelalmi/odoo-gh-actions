# -*- coding: utf-8 -*-
# Imports
import os
import re
import ast

# Message colors
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

# Script parameters
MANIFEST_FILENAMES = ['__manifest__.py', '__openerp__.py']
AUTHOR_NAME = 'e3k'
REQUIRED_KEYS = ['name', 'author', 'version', 'license']
MODULE_NAME_REGEX = r'^[a-z0-9_]+$'
VERSION_REGEX = r'^\d+\.\d+\.\d+$'


def preprocess_manifest(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        lines = content.split('\n')

    json_content = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            json_content.append(line)

    # Join the content and replace single quotes with double quotes
    json_string = ''.join(json_content)
    json_string = re.sub(r"'", r'"', json_string)

    # Remove trailing commas before closing braces/brackets
    json_string = re.sub(r',(\s*[}\]])', r'\1', json_string)

    return json_string


def validate_manifest(manifest_path):
    manifest_content = preprocess_manifest(manifest_path)
    try:
        manifest = ast.literal_eval(manifest_content)
    except (SyntaxError, ValueError) as e:
        return [f"Error decoding manifest in {manifest_path}: {str(e)}"]

    module_name = os.path.basename(os.path.dirname(manifest_path))
    author = manifest.get('author', '')
    version = manifest.get('version', '')
    python_dependencies = manifest.get('external_dependencies', {}).get('python', [])

    errors = []

    for key in REQUIRED_KEYS:
        if key not in manifest or not manifest[key]:
            errors.append(f"Module {module_name}: missing required key '{key}'.")

    if module_name.startswith(AUTHOR_NAME) and author != AUTHOR_NAME:
        errors.append(f"Module {module_name}: author must be '{AUTHOR_NAME}'.")

    if not re.match(MODULE_NAME_REGEX, module_name):
        errors.append(f"Module {module_name}: name contains special characters or uppercase letters.")

    if not re.match(VERSION_REGEX, version):
        errors.append(f"Module {module_name}: version must be in format x.x.x.")

    if python_dependencies:
        requirements_file = 'requirements.txt'
        if not os.path.isfile(requirements_file):
            errors.append(f"Module {module_name}: python dependencies are specified but requirements.txt is missing.")
        else:
            with open(requirements_file) as file:
                requirements_content = file.read()
                for python_dep in python_dependencies:
                    if python_dep not in requirements_content:
                        errors.append(f"Module {module_name}: python dependency '{python_dep}' is missing in requirements.txt.")

    return errors


def main():
    errors = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == '__manifest__.py' or file == '__openerp__.py':
                manifest_path = os.path.join(root, file)
                errors.extend(validate_manifest(manifest_path))

    if errors:
        for error in errors:
            print(f"{RED}{error}{RESET}")
        exit(1)  # Exit with a non-zero status to indicate failure

    print(f"{GREEN}All manifests are valid.{RESET}")
    exit(0)  # Exit with zero status to indicate success


if __name__ == "__main__":
    main()
