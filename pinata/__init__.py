from pinata.api_key import set_keys_from_prompt
from pinata.exceptions import PinataMissingAPIKeyError
from pinata.sdk import Pinata


def create_pinata(profile_name: str) -> Pinata:
    """
    Get or create a Pinata SDK instance with the given profile name.
    If the profile does not exist, you will be prompted to create one,
    which means you will be prompted for your API key and secret. After
    that, they will be stored securely using ``keyring`` and accessed
    as needed without prompt.

    Args:
        profile_name (str): The name of the profile to get or create.

    Returns:
        :class:`~pinata.sdk.Pinata`
    """

    try:
        pinata = Pinata.from_profile_name(profile_name)
    except PinataMissingAPIKeyError:
        set_keys_from_prompt(profile_name)
        pinata = Pinata.from_profile_name(profile_name)

    if not pinata:
        set_keys_from_prompt(profile_name)

    return Pinata.from_profile_name(profile_name)


__all__ = ["Pinata", "create_pinata"]
