import json
from datetime import datetime
from pathlib import Path
from typing import IO, Dict, Union


def format_dict(dict_, label=None):
    indented_dict = json.dumps(dict_, indent=4)
    res = f"{label} {indented_dict}" if label else indented_dict
    return res


def prettify_date(date_str: str):
    date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date.strftime("%Y-%m-%d %H:%M:%S")


def json_to_dict(json_arg: Union[Path, IO, Dict]):
    if not json_arg:
        raise ValueError(f"Non-empty dict-like argument required - was given '{json_arg}'.")

    def _get_json_from_file(file: IO) -> Dict:
        try:
            return json.load(file)
        except json.JSONDecodeError as err:
            raise ValueError(f"File at path '{json_arg}' is not JSON.") from err

    if isinstance(json_arg, Path):
        if not json_arg.exists():
            raise ValueError(f"File '{json_arg}' does not exist.")

        with open(str(json_arg)) as json_file:
            return _get_json_from_file(json_file)

    elif not isinstance(json_arg, dict):
        return _get_json_from_file(json_arg)

    return json_arg
