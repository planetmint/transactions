# Copyright © 2020 Interplanetary Database Association e.V.,
# Planetmint and IPDB software contributors.
# SPDX-License-Identifier: (Apache-2.0 AND CC-BY-4.0)
# Code is Apache-2.0 and docs are CC-BY-4.0

import base58
import base64
import time
import re
import rapidjson
from typing import Callable

# from planetmint.config import Config
from transactions.common.exceptions import ValidationError
from planetmint_cryptoconditions import ThresholdSha256, Ed25519Sha256, ZenroomSha256, Fulfillment
from transactions.common.exceptions import ThresholdTooDeep
from planetmint_cryptoconditions.exceptions import UnsupportedTypeError

VALID_LANGUAGES = (
    "danish",
    "dutch",
    "english",
    "finnish",
    "french",
    "german",
    "hungarian",
    "italian",
    "norwegian",
    "portuguese",
    "romanian",
    "russian",
    "spanish",
    "swedish",
    "turkish",
    "none",
    "da",
    "nl",
    "en",
    "fi",
    "fr",
    "de",
    "hu",
    "it",
    "nb",
    "pt",
    "ro",
    "ru",
    "es",
    "sv",
    "tr",
)


def gen_timestamp() -> str:
    """The Unix time, rounded to the nearest second.
    See https://en.wikipedia.org/wiki/Unix_time

    Returns:
        str: the Unix time
    """
    return str(round(time.time()))


def serialize(data: dict) -> str:
    """Serialize a dict into a JSON formatted string.

    This function enforces rules like the separator and order of keys.
    This ensures that all dicts are serialized in the same way.

    This is specially important for hashing data. We need to make sure that
    everyone serializes their data in the same way so that we do not have
    hash mismatches for the same structure due to serialization
    differences.

    Args:
        data (dict): dict to serialize

    Returns:
        str: JSON formatted string

    """
    return rapidjson.dumps(data, skipkeys=False, ensure_ascii=False, sort_keys=True)


def deserialize(data: str) -> dict:
    """Deserialize a JSON formatted string into a dict.

    Args:
        data (str): JSON formatted string.

    Returns:
        dict: dict resulting from the serialization of a JSON formatted
        string.
    """
    return rapidjson.loads(data)


def validate_all_items_in_list(obj_name: str, data: list, validation_fun: Callable) -> None:
    for item in data:
        if isinstance(item, dict):
            validate_all_keys_in_obj(obj_name, item, validation_fun)
        elif isinstance(item, list):
            validate_all_items_in_list(obj_name, item, validation_fun)


def validate_all_keys_in_obj(obj_name: str, obj: dict, validation_fun: Callable) -> None:
    """Validate all (nested) keys in `obj` by using `validation_fun`.

    Args:
        obj_name (str): name for `obj` being validated.
        obj (dict): dictionary object.
        validation_fun (function): function used to validate the value
        of `key`.

    Returns:
        None: indicates validation successful

    Raises:
        ValidationError: `validation_fun` will raise this error on failure
    """
    for key, value in obj.items():
        validation_fun(obj_name, key)
        if isinstance(value, dict):
            validate_all_keys_in_obj(obj_name, value, validation_fun)
        elif isinstance(value, list):
            validate_all_items_in_list(obj_name, value, validation_fun)


def validate_all_values_for_key_in_obj(obj: dict, key: str, validation_fun: Callable) -> None:
    """Validate value for all (nested) occurrence  of `key` in `obj`
    using `validation_fun`.

     Args:
         obj (dict): dictionary object.
         key (str): key whose value is to be validated.
         validation_fun (function): function used to validate the value
         of `key`.

     Raises:
         ValidationError: `validation_fun` will raise this error on failure
    """
    for vkey, value in obj.items():
        if vkey == key:
            validation_fun(value)
        elif isinstance(value, dict):
            validate_all_values_for_key_in_obj(value, key, validation_fun)
        elif isinstance(value, list):
            validate_all_values_for_key_in_list(value, key, validation_fun)


def validate_all_values_for_key_in_list(input_list: list, key: str, validation_fun: Callable) -> None:
    for item in input_list:
        if isinstance(item, dict):
            validate_all_values_for_key_in_obj(item, key, validation_fun)
        elif isinstance(item, list):
            validate_all_values_for_key_in_list(item, key, validation_fun)


def validate_key(obj_name: str, key: str) -> None:
    """Check if `key` contains ".", "$" or null characters.

    https://docs.mongodb.com/manual/reference/limits/#Restrictions-on-Field-Names

     Args:
         obj_name (str): object name to use when raising exception
         key (str): key to validated

     Returns:
         None: validation successful

     Raises:
         ValidationError: will raise exception in case of regex match.
    """
    if re.search(r"^[$]|\.|\x00", key):
        error_str = (
            'Invalid key name "{}" in {} object. The '
            "key name cannot contain characters "
            '".", "$" or null characters'
        ).format(key, obj_name)
        raise ValidationError(error_str)


def _fulfillment_to_details(fulfillment: type[Fulfillment]) -> dict:
    """Encode a fulfillment as a details dictionary

    Args:
        fulfillment: Crypto-conditions Fulfillment object
    """

    if fulfillment.type_name == "ed25519-sha-256":
        return {
            "type": "ed25519-sha-256",
            "public_key": base58.b58encode(fulfillment.public_key).decode(),
        }

    if fulfillment.type_name == "threshold-sha-256":
        subconditions = [_fulfillment_to_details(cond["body"]) for cond in fulfillment.subconditions]
        return {
            "type": "threshold-sha-256",
            "threshold": fulfillment.threshold,
            "subconditions": subconditions,
        }
    if fulfillment.type_name == "zenroom-sha-256":
        return {
            "type": "zenroom-sha-256",
            "public_key": base58.b58encode(fulfillment.public_key).decode(),
            "script": base58.b58encode(fulfillment.script).decode(),
            "data": base58.b58encode(fulfillment.data).decode(),
        }

    raise UnsupportedTypeError(fulfillment.type_name)


def _fulfillment_from_details(data: dict, _depth: int = 0):
    """Load a fulfillment for a signing spec dictionary

    Args:
        data: tx.output[].condition.details dictionary
    """
    if _depth == 100:
        raise ThresholdTooDeep()

    if data["type"] == "ed25519-sha-256":
        public_key = base58.b58decode(data["public_key"])
        return Ed25519Sha256(public_key=public_key)

    if data["type"] == "threshold-sha-256":
        threshold = ThresholdSha256(data["threshold"])
        for cond in data["subconditions"]:
            cond = _fulfillment_from_details(cond, _depth + 1)
            threshold.add_subfulfillment(cond)
        return threshold

    if data["type"] == "zenroom-sha-256":
        public_key_ = base58.b58decode(data["public_key"])
        script_ = base58.b58decode(data["script"])
        data_ = base58.b58decode(data["data"])
        # TODO: assign to zenroom and evaluate the outcome
        ZenroomSha256(script=script_, data=data_, keys={public_key_})

    raise UnsupportedTypeError(data.get("type"))


def validate_language(value):
    """Check if `value` is a valid language.
    https://docs.mongodb.com/manual/reference/text-search-languages/

     Args:
         value (str): language to validated

     Returns:
         None: validation successful

     Raises:
         ValidationError: will raise exception in case language is not valid.
    """
    if value not in VALID_LANGUAGES:
        error_str = (
            "MongoDB does not support text search for the "
            'language "{}". If you do not understand this error '
            'message then please rename key/field "language" to '
            'something else like "lang".'
        ).format(value)
        raise ValidationError(error_str)


def key_from_base64(base64_key):
    return base64.b64decode(base64_key).hex().upper()


def public_key_to_base64(ed25519_public_key):
    return key_to_base64(ed25519_public_key)


def key_to_base64(ed25519_key):
    ed25519_key = bytes.fromhex(ed25519_key)
    return base64.b64encode(ed25519_key).decode("utf-8")
