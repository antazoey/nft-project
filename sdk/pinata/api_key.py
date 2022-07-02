import json
from typing import Dict, List, Tuple

import click
import keyring

from pinata.exceptions import PinataMissingAPIKeyError

SERVICE_NAME = "pinata"
PINATA_MGMT_KEY = "pinata-mgmt"
PROFILES_KEY = "profiles"
DEFAULT_KEY = "default"


def set_keys_from_prompt(profile_name: str):
    """
    Create an API key profile from a ``click.prompt()``.
    Useful for scripting the creating of profiles.

    Args:
        profile_name (str): The profile name to use.
    """

    api_key = click.prompt("Enter your Pinata API key")
    api_secret = click.prompt("Enter your Pinata API key secret")
    manager = get_key_manager()
    manager.set_key_pair(profile_name, api_key, api_secret)


def _set_mgmt_dict(new_mgmt_dict: Dict):
    new_mgmt_str = json.dumps(new_mgmt_dict)
    keyring.set_password(SERVICE_NAME, PINATA_MGMT_KEY, new_mgmt_str)


def _add_profile_to_mgmt(profile_name: str, mgmt: Dict):
    if PROFILES_KEY not in mgmt or not mgmt[PROFILES_KEY]:
        mgmt[PROFILES_KEY] = [profile_name]
    else:
        mgmt[PROFILES_KEY].append(profile_name)

    _set_mgmt_dict(mgmt)


def _get_password(username: str):
    return keyring.get_password(SERVICE_NAME, username)


def _delete_password(username: str):
    keyring.delete_password(SERVICE_NAME, username)


class KeyringManager:
    """
    A class that manages your API keys. Create API key profiles to use in your scripts.
    """

    @property
    def mgmt(self) -> Dict:
        """
        A dictionary that will for sure have the keys ``"profiles"`` that
        is a list of managed profile names and ``"default"`` which points
        to one of those profile names. There will always be a default if
        there is at least 1 managed profile name.
        """

        mgmt_str = _get_password(PINATA_MGMT_KEY) or ""

        # Initialize the MGMT JSON if it does not already exist.
        if not mgmt_str:
            init_mgmt = {PROFILES_KEY: [], DEFAULT_KEY: None}
            _set_mgmt_dict(init_mgmt)
            return init_mgmt

        mgmt_dict = json.loads(mgmt_str) if mgmt_str else {}
        if PROFILES_KEY not in mgmt_dict:
            mgmt_dict[PROFILES_KEY] = []
        if DEFAULT_KEY not in mgmt_dict:
            mgmt_dict[DEFAULT_KEY] = ""

        # If the default is missing and there is at least 1 profile, set it as default.
        needs_default = (
            mgmt_dict[DEFAULT_KEY] is None or mgmt_dict[DEFAULT_KEY] not in mgmt_dict[PROFILES_KEY]
        )
        if len(mgmt_dict[PROFILES_KEY]) and needs_default:
            mgmt_dict[DEFAULT_KEY] = mgmt_dict[PROFILES_KEY][0]

        return mgmt_dict

    @property
    def profile_names(self) -> List[str]:
        return self.mgmt[PROFILES_KEY]

    @property
    def default_profile_name(self) -> str:
        default_name = self.mgmt[DEFAULT_KEY] or ""
        return default_name

    def set_key_pair(self, profile_name: str, api_key: str, api_key_secret: str):
        """
        Store an API key pair under the given profile name.

        Args:
            profile_name (str): The name of the profile to store the API key pair at.
            api_key (str): The API key.
            api_key_secret (str): The API secret.
        """

        mgmt = dict(self.mgmt)
        if profile_name not in mgmt.get(PROFILES_KEY, []):
            _add_profile_to_mgmt(profile_name, mgmt)

        keyring.set_password(SERVICE_NAME, f"{profile_name}-api-key", api_key)
        keyring.set_password(SERVICE_NAME, f"{profile_name}-api-secret", api_key_secret)

    def delete_key_pair(self, profile_name: str):
        """
        Remove an API key pair.

        Args:
            profile_name (str): The API key profile to remove.
        """

        mgmt = dict(self.mgmt)
        if profile_name in mgmt.get(PROFILES_KEY, []):
            mgmt[PROFILES_KEY].remove(profile_name)
            _set_mgmt_dict(mgmt)

        _delete_password(f"{profile_name}-api-key")
        _delete_password(f"{profile_name}-api-secret")

    def get_key_pair(self, profile_name: str) -> Tuple[str, str]:
        """
        Get an API key pair for authenticating.

        Args:
            profile_name (str): The name of the API key profile to get.

        Returns:
            Tuple[str, str]
        """

        api_key = _get_password(f"{profile_name}-api-key")
        api_secret = _get_password(f"{profile_name}-api-secret")

        if not api_key or not api_secret:
            raise PinataMissingAPIKeyError(profile_name)

        # Add the profile to MGMT JSON if it for some reason is missing.
        mgmt = dict(self.mgmt)
        if api_key and api_secret and profile_name not in mgmt.get(PROFILES_KEY, []):
            _add_profile_to_mgmt(profile_name, mgmt)

        return api_key, api_secret

    def rename_key_pair(self, old_name: str, new_name: str):
        """
        Rename an API key profile.

        Args:
            old_name (str): The name of the profile to change.
            new_name (str): The new name of the profile.
        """
        api_key, api_secret = self.get_key_pair(old_name)
        self.set_key_pair(new_name, api_key, api_secret)
        self.delete_key_pair(old_name)

        # Change the default if needed.
        if self.default_profile_name == old_name:
            mgmt = dict(self.mgmt)
            mgmt[DEFAULT_KEY] = new_name
            _set_mgmt_dict(mgmt)


def get_key_manager():
    return KeyringManager()


__all__ = ["get_key_manager", "set_keys_from_prompt"]
