# 2. Write a Custom Manifest

In [part 1](1-validate.md), we validated an example fileset against a pre-defined manifest, to check if it was valid.
In this section, we will write a custom manifest that anyone can use to check if their fileset is valid according to our rules.

You might want to do this if you are a researcher who wants to check the validitiy of their dataset before uploading it to a repository, or if you are a repository maintainer who wants to check the validity of a dataset before accepting it.
Or, you might be a lab manager who wants to implement data sharing best practices in your lab, and wants to create a set of lab-specific data types that all lab members can use to validate their data.

## 1.1. Prerequisites

It is recommended that you complete [tutorial part 1](1-validate.md) before continuing, so that you understand how to validate a fileset using the File Validator.

For this section, we'll re-use the `my_fileset` fileset that we created in the previous section.
If you don't have a `my_fileset` directory, you can create one using the shell commands:

<!-- termynal -->

```console
$ mkdir my_fileset
$ mkdir my_fileset/my_subject
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

my_fileset/my_subject:
$ export MY_FILESET_PATH="$(pwd)/my_fileset"
$ echo "My fileset path is: $MY_FILESET_PATH"
```

## 1.2. Create a Manifest

The rest of this tutorial will focus on writing a manifest file for a custom fileset type.
We'll call this type `my_type`, and we'll create a manifest for it called `my_type.yaml`.

In your favorite text editor, create a new file called `my_type.yaml` and add the following contents:

```{.yaml linenums="1"}
--8<-- "snippets/my_type.yaml::8"
```

Let's break down this manifest file line-by-line:

- Line 1 defines the `id` of the manifest, which _should_ be unique across all manifests (including ones contributed by other community members).
- Line 2 defines the `version` of the manifest, which _should_ follow [semantic versioning](https://semver.org/).
- Lines 3-5 defines a human-readable `description` of the manifest. Since this file is written in YAML, we can use the `>` character to write a multi-line description. See [online documentation about YAML](https://yaml-multiline.info/) for more details.
- Lines 6-8 describes the `author` of the manifest, including their name and email.

Notice that we have not yet defined any rules in our manifest; we'll get to this soon.
Note that a manifest file without any rules is still valid, and can therefore be used to validate a fileset.
You can test this yourself by validating `my_fileset` against `my_type.yaml` using the CLI:

<!-- termynal -->

```console
$ datajoint-file-validator validate $MY_FILESET_PATH my_type.yaml
✔ Validation successful!
```

Because our manifest has no rules, it will accept any fileset as valid.

Assuming we are in the same directory as the `my_type.yaml` manifest, this manifest is now discoverable using `find_manifest` in the Python API or the `manifest list` CLI command:

<!-- termynal -->

```console
$ datajoint-file-validator manifest list --query 'my_type'
┏━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ ID      ┃ Version ┃ Description ┃ Path         ┃
┡━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ my_type │ 0.1.0   │             │ my_type.yaml │
└─────────┴─────────┴─────────────┴──────────────┘
```

## 1.3. Add a Rule to the Manifest

Now that we have a manifest, we can add rules to it.
Rules are defined using the `rules` key in the manifest, which is a list of rules.
Let's start by defining a simple rule: we want to ensure that there are at least 3 files (not including subdirectories themselves) anywhere in the fileset.
Append a `rules` section so that your manifest looks like this:

```{.yaml linenums="1"}
--8<-- "snippets/my_type.yaml::15"
```

Like the manifest, this rule has an `id` (which _should_ be unique), and human-readable `description`.
Both of these fields are optional, but recommended, especially if you are writing a manifest that will be used by others.
On line 15, we define the `count_min` field, which contains the logic that checks if our rule is valid
Formally, we call this `count_min` field a **constraint**, and it is one of several types of constraints that we can use to define rules.

If we validate our fileset again, we'll see that it is still valid against our manifest because it has at least 3 files:

<!-- termynal -->

```console
$ datajoint-file-validator validate $MY_FILESET_PATH my_type.yaml
✔ Validation successful!
```

We can add another constraint to our rule.
This time, we'll use the `count_max` constraint to ensure that there are no more than 3 files in the fileset:

```{.yaml linenums="1"}
--8<-- "snippets/my_type.yaml::15"
      count_max: 3
```

Since our fileset has 4 files, it now fails validation because all constraints in a rule must be satisfied:

<!-- termynal -->

```console
$ datajoint-file-validator validate $MY_FILESET_PATH my_type.yaml
❌ Validation failed with 1 errors!
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Rule ID        ┃ Rule Description     ┃ Constraint ID ┃ Constraint Value ┃ Errors                ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━┩
│ my_simple_rule │ A simple rule that   │ count_max     │ 3                │ constraint            │
│                │ checks that there    │               │                  │ `count_max` failed: 5 │
│                │ are at least 3 files │               │                  │ > 3                   │
│                │ (not including       │               │                  │                       │
│                │ subdirectories       │               │                  │                       │
│                │ themselves) anywhere │               │                  │                       │
│                │ in the fileset.      │               │                  │                       │
│                │                      │               │                  │                       │
└────────────────┴──────────────────────┴───────────────┴──────────────────┴───────────────────────┘
```

We can increase `count_max` to 5 to make our fileset valid again:

```{.yaml linenums="1"}
--8<-- "snippets/my_type.yaml::16"
```

<!-- termynal -->

```console
$ datajoint-file-validator validate $MY_FILESET_PATH my_type.yaml
✔ Validation successful!
```

## 1.4. Queries

Our manifest is already useful with a single rule, with two constraints that check the minimum number of files.
Let's add another more complicated rule, so that our manifest looks like this:

```{.yaml linenums="1"}
--8<-- "snippets/my_type.yaml::23"
```

On line 21, we define a `query` field in the rule.
This field uses a glob pattern to filter the list of files, before they are validated against the constraints: `count_min` and `count_max`.
In this case, `*.txt` matches only files that are at the top level of the fileset (`*`), and end with the `.txt` extension.
After filtering, the only file that matches this query is `observations.txt`, which is the only file that is validated against the constraints.

!!! note

    If `query` is not defined for a rule, it is automatically set to the default value of `**`, which matches all files in the fileset.

Suppose that we wanted to check the number of `.csv` files _anywhere_ in the fileset, not just at the top level.
We can define another rule to check this, now using the `**.csv` query that matches all `.csv` files anywhere in the fileset.
Append to the manifest `rules`:

```{.yaml linenums="1"}
--8<-- "snippets/my_type.yaml:24:30"
```

Since the `**/*.csv` query matches two files, `my_subdirectory/subject1.csv` and `my_subdirectory/subject2.csv` (it will also match `.csv` files at the top level, if there were any), the `count_min` constraint is satisfied.
For more details on how to write glob-style queries, see online resources such as [this article from VS Code](https://code.visualstudio.com/docs/editor/glob-patterns) and the [wcmatch documentation](https://facelessuser.github.io/wcmatch/wcmatch/) (which is the library that File Validator uses).

<!-- termynal -->

```console
$ datajoint-file-validator validate $MY_FILESET_PATH my_type.yaml
✔ Validation successful!
```

## 1.5. Regex Constraints

## Test Tabs

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
--8<-- "snippets/manifests/demo_dlc/default.yaml"
```

</details>

