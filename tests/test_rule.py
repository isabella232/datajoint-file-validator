import pytest
from copy import deepcopy
from datajoint_file_validator.rule import Rule
from datajoint_file_validator.yaml import read_yaml
from datajoint_file_validator.error import InvalidRuleError


# {
#     "id": "test",
#     "version": "0.1",
#     "description": "Test manifest",
#     "rules": [
#         {
#             "id": "count_min_max",
#             "description": "Check count min max",
#             "query": "**",
#             "count_min": 20,
#         },
#         {
#             # id automatically generated from hash of constraints
#             "count_max": 3,
#         },
#         {
#             "id": "max_txt_files",
#             "query": "*.txt",
#             "count_max": 5,
#         },
#         {
#             "eval": "def test_custom(snapshot):\n    return False",
#         },
#     ],
# }


class TestRule:
    def test_all_registry_rules_valid(self, manifest_file_from_registry: str):
        """
        Checks that all rules in all manifests in the registry are valid.
        """
        mani_dict = read_yaml(manifest_file_from_registry)
        for rule_dict in mani_dict.get("rules", list()):
            Rule.from_dict(rule_dict)

    def test_valid_rule_basic(self):
        Rule.from_dict(
            {
                "id": "test",
                "description": "Test rule",
                "query": "**",
                "count_min": 20,
            }
        )

    def test_valid_rule_empty(self):
        Rule.from_dict(dict())

    def test_valid_rule_no_constraint(self):
        Rule.from_dict(
            {
                "id": "test",
                "description": "Test rule",
                "query": "**",
            }
        )

    def test_valid_rule_no_query(self):
        Rule.from_dict(
            {
                "id": "test",
                "description": "Test rule",
            }
        )

    def test_valid_rule_str_value(self):
        """
        Also a valid rule, even though the annotation for CountMinConstraint.val
        is int. End user wouldn't encounter this in practice, because this
        is checked by Manifest.check_valid against the manifest schema.
        """
        Rule.from_dict(
            {
                "id": "test",
                "description": "Test rule",
                "query": "**",
                "count_min": "not a number",
            }
        )

    def test_invalid_rule_unknown_constraint(self):
        with pytest.raises(InvalidRuleError) as e:
            Rule.from_dict(
                {
                    "id": "test",
                    "description": "Test rule",
                    "query": "**",
                    "non_existent_constraint": 2,
                }
            )
        assert "unknown constraint" in str(e.value).lower(), str(e.value)

    def test_invalid_rule_invalid_query(self):
        with pytest.raises(InvalidRuleError) as e:
            Rule.from_dict(
                {
                    "id": "test",
                    "description": "Test rule",
                    "query": 189,
                }
            )
        assert "query must be a string" in str(e.value).lower(), str(e.value)

    def test_invalid_rule_error_compiling_constraint(self):
        with pytest.raises(InvalidRuleError) as e:
            Rule.compile_constraint(
                name="count_min",
                val="not a number",
                constraint_map=dict(count_min=(lambda: None)),
            )

    def test_invalid_rule_error_composite_query(self):
        with pytest.raises(InvalidRuleError) as e:
            Rule.from_dict(
                {
                    "id": "test",
                    "description": "Test rule",
                    "query": {},
                }
            )
        assert "empty" in str(e.value).lower(), str(e.value)
