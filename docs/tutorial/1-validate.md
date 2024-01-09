# 1. Validate a Fileset

Welcome to the DataJoint File Validator tutorial!
In this section, we will walk through the process of validating a set of files, to check if they match the expected format.
You might want to do this if you are, for example, a researcher who wants to check that your data files are in the correct format before uploading them to the DataJoint platform or sharing them with others in your research group.
Or, you might be a developer who wants to check that your code is generating files in the correct format.

## 1.1. Install the File Validator

The File Validator is a Python package that you can install using `pip`.
Please note that the File Validator requires Python 3.7 or later.

<!-- termynal -->

```console
$ pip install git+https://github.com/ethho/datajoint-file-validator.git
---> 100%
Successfully installed datajoint-file-validator-0.0.1
```

## 1.2. Create a Fileset

We need a set of one or more files to validate.
This can be a set of files that you have already created, or you can create a new set of files for this tutorial.

For this tutorial, we will create an example fileset in the shell:

```console
$ mkdir my_fileset
$ mkdir my_fileset/my_subdirectory
$ touch my_fileset/observations.txt
$ touch my_fileset/my_subdirectory/subject1.csv
$ touch my_fileset/my_subdirectory/subject2.csv
$ touch my_fileset/my_subdirectory/subject3.txt
```

We can now check the contents of the fileset, and save the path to the fileset for later:

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

!!! note

    Some terminology before we continue:

    Formally, we call the "expected format" of a fileset its **fileset type**.
    A fileset type is defined by a **manifest**, which is a YAML file that describes the expected structure of the fileset.
    We say that a fileset is **valid** if it matches the expected structure described by its manifest.

For the purposes of this tutorial, we will use an example fileset type called `demo_tutorial`, whose manifest file is included in the File Validator package.
We can use either the Python API or the included command line interface (CLI) to validate the fileset:

!!! example "Validate the Fileset"

    === "Python"

        We'll start by opening a Python interactive shell and importing the `validate` function from the File Validator package:

        ```console
        $ python3
        Python 3.11.4 (main, Dec  7 2023, 15:43:41) [GCC 12.3.0] on linux
        Type "help", "copyright", "credits" or "license" for more information.
        >>> from datajoint_file_validator import validate, find_manifest
        ```

        Next, import the path to the example fileset we created earlier:

        ```python3
        >>> import os
        >>> my_dataset_path = os.environ['MY_FILESET_PATH']
        >>> print(my_dataset_path)
        /some/path/to/my_fileset
        ```

        We can set the path to the manifest file as a string, or we can use the `find_manifest` function which will attempt to find the manifest file automatically:

        ```python3
        >>> manifest_path = find_manifest('demo_tutorial/v1')
        >>> print(manifest_path)
        /some/path/to/demo_tutorial/v1.yaml
        ```

        Now we can validate the fileset using the `validate` function:

        ```python3
        >>> success, report = validate(my_dataset_path, manifest_path)
        >>> print(success)
        True
        >>> print(report)
        []
        >>>
        ```

    === "CLI"

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

# Test Tabs

=== "C"

    ``` c
    #include <stdio.h>

    int main(void) {
      printf("Hello world!\n");
      return 0;
    }
    ```

=== "C++"

    ``` c++
    #include <iostream>

    int main(void) {
      std::cout << "Hello world!" << std::endl;
      return 0;
    }
    ```

## Inspect a Manifest

<details>
<summary> <code>manifests/demo_dlc/default.yaml</code> </summary>

```{.yaml linenums="1"}
--8<-- "manifests/demo_dlc/default.yaml"
```

</details>