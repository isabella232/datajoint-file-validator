# DataJoint File Validator

This repository contains a Python package that validates file sets for DataJoint pipelines.

## Installation

```bash
pip install datajoint_file_validator@git+https://github.com/ethho/datajoint-file-validator.git
```

## Quick Start

Validate a fileset against an existing manifest:

```python
from datajoint_file_validator import validate

my_dataset_path = 'tests/data/filesets/fileset0'
manifest_path = 'datajoint_file_validator/manifests/demo_dlc_v0.1.yaml'
success, report = validate(my_dataset_path, manifest_path, verbose=True, format='plain')
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

Alternatively, validate using the included command line interface:

```console
$ datajoint-file-validator validate tests/data/filesets/fileset0 datajoint_file_validator/manifests/demo_dlc_v0.1.yaml
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

## Author

Ethan Ho @ethho

## License

[MIT](LICENSE)