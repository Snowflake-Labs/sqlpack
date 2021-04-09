#!/usr/bin/env python3.9

import re
from itertools import takewhile
from os import path
from typing import Dict, List, Optional
import sys

import yaml
import fire


PACK_PATH = [
    'packs/{0}/main.sql.fmt',
    'packs/{0}/{0}.sql.fmt',
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


def print_sql(pack_name, data_file: Optional[str] = None, **kwargs):
    pack_file_options = [pack_name] + [p.format(pack_name) for p in PACK_PATH]
    pack_file = next((f for f in pack_file_options if path.isfile(f)), None)
    if not pack_file:
        print("NO PACK FOUND WITH NAME", pack_name, file=sys.stderr)
        sys.exit(-1)
    pack_dir = path.dirname(pack_file)
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
