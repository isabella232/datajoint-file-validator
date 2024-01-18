# Basic Usage

_For a comprehensive guide on using the `datajoint-file-validator` package, please see the [tutorial](tutorial/1-validate.md)._

----

As a first step, [install the `datajoint-file-validator` package](installation.md). Optionally, [set up a development environment](contribute.md#set-up-a-development-environment.md).

## Validate Using Python API

Validate an [example fileset](snippets/filesets/fileset0/) against an [example manifest](snippets/manifests/demo_dlc/v0.1.yaml) using the Python API:

```python
from datajoint_file_validator import validate

my_dataset_path = 'tests/data/filesets/fileset0'
manifest_path = 'datajoint_file_validator/manifests/demo_dlc/v0.1.yaml'
success, report = validate(my_dataset_path, manifest_path, verbose=True)
# Validation failed with the following errors:
# [
#     {
#         'rule': 'Min total files',
#         'rule_description': 'Check that there are at least 6 files anywhere in the fileset',
#         'constraint_id': 'count_min',
#         'constraint_value': 6,
#         'errors': 'constraint `count_min` failed: 4 < 6'
#     }
# ]

print(success)
# False
```

## Validate Using the Command Line Interface (CLI)

Alternatively, validate using the included command line interface:

<!-- termynal -->

```console
$ datajoint-file-validator validate tests/data/filesets/fileset0 datajoint_file_validator/manifests/demo_dlc/v0.1.yaml
❌ Validation failed with 1 errors!
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃                ┃ Rule           ┃               ┃ Constraint    ┃                ┃
┃ Rule ID        ┃ Description    ┃ Constraint ID ┃ Value         ┃ Errors         ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ Min total      │ Check that     │ count_min     │ 6             │ constraint     │
│ files          │ there are at   │               │               │ `count_min`    │
│                │ least 6 files  │               │               │ failed: 4 < 6  │
│                │ anywhere in    │               │               │                │
│                │ the fileset    │               │               │                │
└────────────────┴────────────────┴───────────────┴───────────────┴────────────────┘
```

## Next Steps

For a more detailed introduction to the `datajoint-file-validator` package, see the [tutorial](tutorial/1-validate.md).