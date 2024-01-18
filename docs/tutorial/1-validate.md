# 1. Validate a Fileset

Welcome to the DataJoint File Validator tutorial!
In this section, we will walk through the process of validating a set of files, to check if they match the expected format.
You might want to do this if you are a researcher who wants to check that your data files are in the correct format before uploading them to the DataJoint platform, or sharing them with others in your research group.
Or, you might be a developer who wants to check that your code is generating files in the correct format, or that users are submitting files in the correct format.

## 1.1. Install the File Validator

The File Validator is a Python package that you can install using `pip`.
Please note that the File Validator requires Python 3.7 or later.

<!-- termynal -->

```console
$ pip install git+https://github.com/ethho/datajoint-file-validator.git
---> 100%
Successfully installed datajoint-file-validator-0.1.0
```

## 1.2. Create a Fileset

We need a set of one or more files to validate.
This can be a set of files that you have already created, or you can create a new set of files for this tutorial.

For this tutorial, we will create an example fileset in the shell:

<!-- termynal -->

```console
$ mkdir my_fileset
$ mkdir my_fileset/my_subdirectory
$ touch my_fileset/observations.txt
$ touch my_fileset/my_subdirectory/subject1.csv
$ touch my_fileset/my_subdirectory/subject2.csv
$ touch my_fileset/my_subdirectory/subject3.txt
```

We can now check the contents of the fileset, and save the path to the fileset for later:

<!-- termynal -->

```console
$ ls my_fileset/**
my_fileset/observations.txt

my_fileset/my_subdirectory:
subject1.csv  subject2.csv  subject3.txt

$ export MY_FILESET_PATH="$(pwd)/my_fileset"
$ echo "My fileset path is: $MY_FILESET_PATH"
```

## 1.3. Validate the Fileset

Now that we've created an example fileset full of empty files, we can use the File Validator to check that the fileset matches the expected format.

!!! note "A footnote on terminology"

    Formally, we call the "expected format" of a fileset its **fileset type**.
    A fileset type is defined by a **manifest**, which is a YAML file that describes the expected structure of the fileset.
    We say that a fileset is **valid** if it matches the expected structure described by its manifest.

For the purposes of this tutorial, we will use an example fileset type called `demo_tutorial`, whose manifest file is included in the File Validator package.
<!-- We can use either the Python API or the included command line interface (CLI) to validate the fileset.
We'll start with the Python API, and then show how to use the CLI. -->

---

We'll start by opening a Python interactive shell and importing the `validate` function from the File Validator package:

<!-- termynal -->

```console
$ python3
Python 3.11.4 (main, Dec  7 2023, 15:43:41) [GCC 12.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from datajoint_file_validator import validate, find_manifest
```

Next, import the path to the example fileset we created earlier:

<!-- termynal -->

```python3
>>> import os
>>> my_dataset_path = os.environ['MY_FILESET_PATH']
>>> print(my_dataset_path)
/some/path/to/my_fileset
```

We can set the path to the manifest file as a string, or we can use the `find_manifest` function which will attempt to find the manifest file automatically:

<!-- termynal -->

```python3
>>> manifest_path = find_manifest('demo_tutorial/v1')
>>> print(manifest_path)
/some/path/to/demo_tutorial/v1.yaml
```

Now we can validate the fileset using the `validate` function.
We can set the `verbose=True` option to show a table-style report of the validation results:

<!-- termynal -->

```python3
>>> success, report = validate(my_dataset_path, manifest_path, verbose=True)
Validation failed with the following errors:
┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Rule ID      ┃ Rule Description                         ┃ Constraint ID ┃ Constraint Value ┃ Errors                                  ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ rule-3-files │ Check that there are at least 5 files in │ count_min     │ 5                │ constraint `count_min` failed: 4 < 5    │
│              │ the directory (excluding                 │               │                  │                                         │
│              │ subdirectories).                         │               │                  │                                         │
│              │                                          │               │                  │                                         │
├──────────────┼──────────────────────────────────────────┼───────────────┼──────────────────┼─────────────────────────────────────────┤
│ rule-5-regex │ Check that all files in the subdirectory │ regex         │ ^.+\.csv$        │ {'my_subdirectory/subject3.txt':        │
│              │ are .csv files                           │               │                  │ {'path': ["value does not match regex   │
│              │                                          │               │                  │ '^.+\\.csv$'"]}}                        │
└──────────────┴──────────────────────────────────────────┴───────────────┴──────────────────┴─────────────────────────────────────────┘
```

We see that our example fileset failed validation against the `demo_tutorial` fileset type.
The validation report shows us that the fileset failed two rules:

1. `rule-3-files`: The fileset contains only 4 files total, not 5 as required in the manifest.
2. `rule-5-regex`: The `my_subdirectory` subdirectory contains a file that does not match the expected regex pattern: it ends with the `.txt` instead of `.csv`.

<!-- If this were a fileset that we were about to upload to the DataJoint platform, we would want to fix these errors before uploading the fileset. -->

We can also inspect the validation results as a Python object, which is useful for validating programmatically:

<!-- termynal -->

```python3
>>> print(success)
False
>>> from pprint import pprint
>>> pprint(report)
[{'constraint_id': 'count_min',
  'constraint_value': 5,
  'errors': 'constraint `count_min` failed: 4 < 5',
  'rule': 'rule-3-files',
  'rule_description': 'Check that there are at least 5 files in the directory '
                      '(excluding subdirectories).\n'},
 {'constraint_id': 'regex',
  'constraint_value': '^.+\\.csv$',
  'errors': {'my_subdirectory/subject3.txt': {'path': ['value does not match '
                                                       "regex '^.+\\.csv$'"]}},
  'rule': 'rule-5-regex',
  'rule_description': 'Check that all files in the subdirectory are .csv '
                      'files'}]
```

## 1.4. Fixing Errors in the Fileset and Re-Validating

Now that we know what errors are present in the fileset, we can fix them.
In a real-world scenario, validation failure could indicate that we have forgotten or misnamed a file that is required for downstream analysis.
Therefore, in practice, the measures you take to fix errors will depend on your specific use case.
In this example use case, we will

1. Add a new file to the fileset, so that we satisfy rule `rule-3-files`, and
2. Rename the file that does not match the regex pattern, to satisfy rule `rule-5-regex`.

<!-- termynal -->

```console
$ touch my_fileset/more_observations.txt
$ mv my_fileset/my_subdirectory/subject3.txt my_fileset/my_subdirectory/subject3.csv
$ ls my_fileset/**
my_fileset/more_observations.txt  my_fileset/observations.txt

my_fileset/my_subdirectory:
subject1.csv  subject2.csv  subject3.csv
```

We can now re-validate the fileset:

<!-- termynal -->

```python3
>>> success, report = validate(my_dataset_path, manifest_path, verbose=True)
>>> print(success)
True
>>> print(report)
[]
```

We see that the fileset now passes validation, and the validation report is empty!

## 1.5. Validate the Fileset using the CLI

As an alternative to using the Python API, we can also validate the fileset using the included command line interface (CLI).
For the sake of demonstration, we'll remove one of our files, so that the fileset will fail validation:

<!-- termynal -->

```console
$ rm my_fileset/my_subdirectory/subject1.csv
$ ls my_fileset/**
my_fileset/more_observations.txt  my_fileset/observations.txt

my_fileset/my_subdirectory:
subject2.csv  subject3.csv
```

We can now validate the fileset using the CLI:

<!-- termynal -->

```console
$ datajoint-file-validator validate $MY_FILESET_PATH demo_tutorial/v1
❌ Validation failed with 1 errors!
┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Rule ID      ┃ Rule Description       ┃ Constraint ID ┃ Constraint Value ┃ Errors                ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━┩
│ rule-3-files │ Check that there are   │ count_min     │ 5                │ constraint            │
│              │ at least 5 files in    │               │                  │ `count_min` failed: 4 │
│              │ the directory          │               │                  │ < 5                   │
│              │ (excluding             │               │                  │                       │
│              │ subdirectories).       │               │                  │                       │
│              │                        │               │                  │                       │
└──────────────┴────────────────────────┴───────────────┴──────────────────┴───────────────────────┘
```

We can also output the report in JSON or YAML formats, and save it to a file:

<!-- termynal -->

```console
$ datajoint-file-validator validate --format json $MY_FILESET_PATH demo_tutorial/v1
❌ Validation failed with 1 errors!
[
  {
    "rule": "rule-3-files",
    "rule_description": "Check that there are at least 5 files in the directory (excluding subdirectories).\n",
    "constraint_id": "count_min",
    "constraint_value": 5,
    "errors": "constraint `count_min` failed: 4 < 5"
  }
]

$ datajoint-file-validator validate --format yaml $MY_FILESET_PATH demo_tutorial/v1 > report.yaml
❌ Validation failed with 1 errors!

$ cat report.yaml
- constraint_id: count_min
  constraint_value: 5
  errors: 'constraint `count_min` failed: 4 < 5'
  rule: rule-3-files
  rule_description: 'Check that there are at least 5 files in the directory
    (excluding subdirectories).'
```

Once again, we can fix the errors in the fileset and re-validate:

<!-- termynal -->

```console
$ touch my_fileset/my_subdirectory/subject6.csv # add a new file to pass validation
$ datajoint-file-validator validate $MY_FILESET_PATH demo_tutorial/v1
✔ Validation successful!
```

## 1.6. List Available Manifests

Although the File Validator package gives you a toolbox for creating your own manifest files for custom fileset types, it also includes commonly used fileset types that you can use out of the box.
These include manifests contributed by the DataJoint team and the community.
You can list the available manifests using the `list_manifests` function in the Python API, and filter results by passing a regular expression pattern:

<!-- termynal -->

```python3
>>> from datajoint_file_validator import list_manifests
>>> print(f"There are {len(list_manifests())} available manifests.")
There are 4 available manifests.
>>> print(f"There are {len(list_manifests(query='demo_tutorial'))} manifests that match.")
There are 1 manifests that match.
```

Alternatively, use the CLI:

<!-- termynal -->

```console
$ datajoint-file-validator manifest list --query 'demo_tutorial'
┏━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ID            ┃ Version ┃ Description                        ┃ Path                                ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ demo_tutorial │ 0.1.0   │ An example manifest for the        │ /path/to/demo_tutorial/default.yaml │
│               │         │ DataJoint File Validator tutorial. │                                     │
│               │         │                                    │                                     │
└───────────────┴─────────┴────────────────────────────────────┴─────────────────────────────────────┘
```

## 1.7. Inspect a Manifest

We will cover the details of how to write a custom manifest in the [next section](2-manifest.md).
For now, we will inspect the contents of the `demo_tutorial` manifest that we used above.
We see from the `list_manifests` output above that the `demo_tutorial` manifest is located at `/path/to/demo_tutorial/default.yaml` (the actual path to the manifest will be different on your system).
Let's read the contents using `cat /path/to/demo_tutorial/default.yaml` or your favorite text editor:

<!-- termynal -->

<details>
<summary> Output of <code>cat /path/to/demo_tutorial/default.yaml</code> </summary>

```{.yaml linenums="1"}
--8<-- "snippets/manifests/demo_tutorial/v1.yaml"
```

</details>

Again, we'll go into more detail about how to write a custom manifest in the [next section](2-manifest.md).
For now, note that the manifest is a YAML file that contains a list of rules, all of which must pass in order for a fileset to be valid.
Most of these rules passed when we validated our fileset, but the rules with IDs `rule-3-files` (lines 22-29) and `rule-5-regex` (lines 37-40) failed.
Notice that the manifest author has included a `description` of each rule, as well as a `description` of the manifest itself, so that the end user can understand what the manifest is for and what the rules are checking for.

## 1.8. Next Steps

In this section, we learned how to validate a fileset using the File Validator package.
We also learned how to use the included command line interface (CLI) to validate a fileset.
In the [next section](2-manifest.md), we will learn how to write a custom manifest to define a new fileset type.
