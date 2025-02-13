# Copyright © 2020 Interplanetary Database Association e.V.,
# Planetmint and IPDB software contributors.
# SPDX-License-Identifier: (Apache-2.0 AND CC-BY-4.0)
# Code is Apache-2.0 and docs are CC-BY-4.0
import pytest
import json
from transactions.common.script import Script

zenroom_script = """
    Scenario 'test': Script verifies input
    Given that I have a 'string dictionary' named 'houses'
    Then print the string 'ok'
"""

inputs = {
    "houses": [
        {
            "name": "Harry",
            "team": "Gryffindor",
        },
        {
            "name": "Draco",
            "team": "Slytherin",
        },
    ],
}

outputs = ["ok"]

invalid_outputs = ["not ok"]


@pytest.mark.skip(reason="currently not supported")
def test_valid_output():
    script = Script(zenroom_script, inputs, outputs)
    assert script.validate()


@pytest.mark.skip(reason="currently not supported")
def test_invalid_output():
    script = Script(zenroom_script, json.dumps(inputs), invalid_outputs)
    assert not script.validate()


@pytest.mark.skip(reason="currently not supported")
def test_to_dict():
    script = Script(zenroom_script, json.dumps(inputs), outputs)
    script_dict = script.to_dict()
    assert script_dict


@pytest.mark.skip(reason="currently not supported")
def test_from_dict():
    script = Script(zenroom_script, inputs, outputs)
    script_dict = script.to_dict()
    script_from_dict = Script.from_dict(script_dict)
    assert script_from_dict.validate()
