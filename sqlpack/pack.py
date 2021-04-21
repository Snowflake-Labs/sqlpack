#!/usr/bin/env python3.9
import os
import re
from itertools import takewhile
from os import path
from typing import Dict, List, Optional
import sys

import yaml
import fire


PACK_TEMPLATE_PATH= [
    '{0}/packs/{1}/main.sql.fmt',
    '{0}/packs/{1}/{1}.sql.fmt',
]

PACK_YAML_PATH = [
    '{0}/data.yaml',
    '{0}/example_data.yaml',
    '{0}/{1}.yaml',
]


def format(find, replace):
    found = find
    for k in replace:
        found = re.sub(f'{{{k}}}', replace[k], found)
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
    return header['varmap'], header['params']


def print_sql(pack_name, data_file_name: Optional[str] = None, **kwargs):
    cwd = path.dirname(__file__)
    pack_file_options = [pack_name] + [p.format(cwd,pack_name) for p in PACK_TEMPLATE_PATH]
    print(pack_file_options)
    pack_file = next((f for f in pack_file_options if path.isfile(f)), None)
    if not pack_file:
        print("NO PACK FOUND WITH NAME", pack_name, file=sys.stderr)
        sys.exit(-1)
    pack_dir = path.dirname(pack_file)
    data_file_options = [p.format(pack_dir,data_file_name) for p in PACK_YAML_PATH]
    data_file = next((f for f in data_file_options if path.isfile(f)), None)
    template_text = open(pack_file, 'r').read()

    varmap, params = read_template_header(template_text)
    defaults = {p['name']: p['default'] for p in params if 'default' in p}
    for file_datum in load_data_file(data_file):
        args = defaults | varmap | file_datum | kwargs
        missing_params = validate_params(params, args)
        if not missing_params:
            print(expand_macros(pack_dir, format(template_text, args)))
        else:
            for name in missing_params:
                print("MISSING VALUE FOR", name, file=sys.stderr)


if __name__ == '__main__':
    fire.Fire(print_sql)
