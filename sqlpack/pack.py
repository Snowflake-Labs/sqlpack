#!/usr/bin/env python3.9
import re
from itertools import takewhile
from os import path, listdir
from typing import Dict, List, Optional
import sys

import yaml
import fire


SQLPACK_PATH = [
    '../packs/{0}/main.sql.fmt',
    '../packs/{0}/{0}.sql.fmt',
]


def list():
    packs_dir = path.join(path.dirname(__file__), '..', 'packs')
    if path.exists(packs_dir):
        directories = listdir(packs_dir)
        packs = []
        for pack in directories:
            if path.isdir(path.join(packs_dir, pack)):
                content = listdir(path.join(packs_dir, pack))
                if "main.sql.fmt" in content:
                    packs.append(pack)
        packs.sort()
        return packs
    return "Packs directory not found"


def search(pack_name):
    packs = list()
    found_in = []
    for pack in packs:
        if pack_name in pack:
            found_in.append(pack)
    if found_in:
        return found_in
    return f"{pack_name} pack not available. Please refer to https://github.com/Snowflake-Labs/sqlpacks/blob/main/CONTRIBUTING.md if you wish to contribute the {pack_name} pack"


def format(find, replace):
    found = find
    for k in replace:
        found = re.sub(f'{{{k}}}', str(replace[k]), found)
    return find if find == found else format(found, replace)


def expand_macros(pack_dir, pack):
    return re.sub(
        r"USING TEMPLATE '([a-z-_\.]+)'",
        lambda m: f"AS $$\n{open(path.join(pack_dir, m.group(1))).read()}$$",
        pack,
        flags=re.M,
    )


def load_data_file(data_file, **kwargs) -> List[Dict[str, str]]:
    if data_file is None:
        return [{}]

    with open(f"{data_file}", "r") as f:
        data = yaml.safe_load(f)
        if type(data) is list:
            return data
        else:
            return [data]


def validate_params(params: List[Dict[str, str]], arg: Dict[str, str]) -> bool:
    missing_params = set()
    for param in params:
        name = param['name']
        if name not in arg:
            missing_params.add(name)
    return missing_params


def read_template_header(template):
    lines = template.split("\n")
    head = "\n".join(
        re.sub("^-- ", "", l) for l in takewhile(lambda s: s.startswith("-- "), lines)
    )
    header = yaml.safe_load(head)
    try:
        return header['varmap'], header['params']
    except KeyError:
        return "", header['params']


def find_file(file_name, possible_paths, parent_dir='.'):
    possible_files = [file_name] + [p.format(file_name) for p in possible_paths]
    possible_file_paths = [path.join(parent_dir, p) for p in possible_files]
    return next((fp for fp in possible_file_paths if path.isfile(fp)), None)


def print_sample_data(pack_name):
    data_file = path.join(
        path.dirname(__file__), '..', 'packs', pack_name, 'example_data.yaml'
    )
    with open(data_file, 'r') as f:
        print(f.read())


def print_sql(pack_name, data_file=None, **kwargs):
    cwd = path.dirname(__file__)
    pack_file = find_file(pack_name, SQLPACK_PATH, cwd)
    if not pack_file:
        print("NO PACK FOUND WITH NAME", pack_name, file=sys.stderr)
        sys.exit(-1)

    template_text = open(pack_file, 'r').read()
    file_data = load_data_file(data_file) if data_file else [{}]

    varmap, params = read_template_header(template_text)
    pack_dir = path.dirname(pack_file)
    defaults = {p['name']: p['default'] for p in params if 'default' in p}
    for file_datum in file_data:
        if varmap:
            args = defaults | varmap | file_datum | kwargs
        else:
            args = defaults | file_datum | kwargs
        missing_params = validate_params(params, args)
        if not missing_params:
            print(expand_macros(pack_dir, format(template_text, args)))
        else:
            for name in missing_params:
                print("MISSING VALUE FOR", name, file=sys.stderr)
