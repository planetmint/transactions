# Copyright © 2020 Interplanetary Database Association e.V.,
# Planetmint and IPDB software contributors.
# SPDX-License-Identifier: (Apache-2.0 AND CC-BY-4.0)
# Code is Apache-2.0 and docs are CC-BY-4.0

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

def test_valid_output():
    script = Script(zenroom_script, json.dumps(inputs), outputs)
    assert script.validate()

def test_invalid_output():
    script = Script(zenroom_script, json.dumps(inputs), invalid_outputs)
    assert not script.validate()