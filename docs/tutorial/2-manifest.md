# 2. Write a Custom Manifest

In [part 1](1-validate.md), we validated an example fileset against a pre-defined manifest, to check if it was valid.
In this section, we will write a custom manifest that anyone can use to check if their fileset is valid according to our rules.

You might want to do this if you are a researcher who wants to check the validitiy of their dataset before uploading it to a repository, or if you are a repository maintainer who wants to check the validity of a dataset before accepting it.
Or, you might be a lab manager who wants to implement data sharing best practices in your lab, and wants to create a set of lab-specific data types that all lab members can use to validate their data.

## 1.1. Prerequisites

It is recommended that you complete [tutorial part 1](1-validate.md) before continuing, so that you understand how to validate a fileset using the File Validator.

For this section, we'll recreate the `my_fileset` fileset that we created in the previous section.

<!-- termynal -->

```console
$ rm -r my_fileset || true # remove the fileset if it already exists from part 1
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
┏━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ ID      ┃ Version ┃ Description                                       ┃ Path         ┃
┡━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ my_type │ 0.1.0   │ An example fileset type for the DataJoint File    │ my_type.yaml │
│         │         │ Validator tutorial.                               │              │
│         │         │                                                   │              │
└─────────┴─────────┴───────────────────────────────────────────────────┴──────────────┘
```

## 1.3. Add a Rule to the Manifest

Now that we have a manifest, we can add rules to it.
Rules are defined using the `rules` key in the manifest.
Let's start by defining a simple rule: we want to ensure that there are at least 3 files (including subdirectories themselves) anywhere in the fileset.
Append a `rules` section so that your manifest looks like this:

```{.yaml linenums="1"}
--8<-- "snippets/my_type.yaml::15"
```

Like the manifest, this rule has an `id` (which _should_ be unique within the manifest file), and a human-readable `description`.
Both of these fields are optional, but recommended, especially if you are writing a manifest that will be used by others.
On line 15, we define the `count_min` field, which contains the logic that checks if our rule is valid.
Formally, we call this field a **constraint**, and it is one of several types of constraints that we can use.

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
│                │ checks that there    │               │                  │ `count_max` failed: 6 │
│                │ are at least 3 files │               │                  │ > 3                   │
│                │ (including           │               │                  │                       │
│                │ subdirectories       │               │                  │                       │
│                │ themselves) anywhere │               │                  │                       │
│                │ in the fileset.      │               │                  │                       │
│                │                      │               │                  │                       │
└────────────────┴──────────────────────┴───────────────┴──────────────────┴───────────────────────┘
```

We can increase `count_max` to 6 to make our fileset valid again:

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
We can define another rule to check this, now using the `**/*.csv` query that matches all `.csv` files anywhere in the fileset.
Append to the manifest `rules`:

```{.yaml linenums="24"}
--8<-- "snippets/my_type.yaml:24:29"
```

Since the `**/*.csv` query matches two files, `my_subdirectory/subject1.csv` and `my_subdirectory/subject2.csv` (it will also match `.csv` files at the top level, if there were any), the `count_min` constraint is satisfied.
For more details on how to write glob-style queries, see online resources such as [this article from VS Code](https://code.visualstudio.com/docs/editor/glob-patterns) and the [wcmatch documentation](https://facelessuser.github.io/wcmatch/wcmatch/) (which is the library that File Validator uses).

<!-- termynal -->

```console
$ datajoint-file-validator validate $MY_FILESET_PATH my_type.yaml
✔ Validation successful!
```

## 1.5. Complex Queries

So far, we've only used simple glob-style queries to filter the list of files in the fileset.
We can define more complex queries using the `query` field, which accepts `path` and `type` fields.
For example, we can define a query that matches the glob-style pattern `subject`, but excludes directories (only files):

```{.yaml linenums="30"}
--8<-- "snippets/my_type.yaml:30:37"
```

The `path` pattern `**/*subject*` matches `my_directory/subject1.csv`, `my_directory/subject2.csv`, `my_directory/subject3.csv`, and the directory `my_subject/`.
With the `type: file` component, `my_subject/` is excluded from the query, and only the three files are validated against the constraints.

## 1.6. Regex Constraint

So far, we've only used the `count_min` and `count_max` constraints.
We can also use the `regex` constraint to check if file paths match a regular expression.
For example, we can create a new rule that checks that all files in the `my_subdirectory` directory end with the `.csv`  or `.txt` extension:

```{.yaml linenums="38"}
--8<-- "snippets/my_type.yaml:38:45"
```

For details on how to write regular expressions, see online resources such as [regexr.com](https://regexr.com/).

## 1.7. Eval Constraint

Although the built-in constraints give us a lot of flexibility in defining rules, sometimes we need to write custom logic to check if a file is valid.
The `eval` constraint accommodates these use cases by allowing us to write custom Python code to check if a fileset is valid.
The value of `eval` should be a definition of a Python function that:

- Is defined using the `def` syntax, as opposed to `lambda` syntax.
- Takes as its first argument a list of dictionaries, where each dictionary contains information about a file in the fileset.
- Returns a boolean value: `True` if the fileset is valid, and `False` otherwise.

For example, we can define a rule that implements the same logic as our `top_level_txt_files` rule, but uses the `eval` constraint instead of built-in constraints:

```{.yaml linenums="46"}
--8<-- "snippets/my_type.yaml:46:59"
```

When we validate, we see the `STDERR` output from the `print` statement:

<!-- termynal -->

```console
$ datajoint-file-validator validate $MY_FILESET_PATH my_type.yaml
Found .txt file: {'abs_path': '/path/to/my_fileset/observations.txt',
 'atime_ns': 1704917387733281020,
 'ctime_ns': 1704917387125281156,
 'extension': '.txt',
 'last_modified': '2024-01-10T13:09:47.125281+00:00',
 'mtime_ns': 1704917387125281156,
 'name': 'observations.txt',
 'path': 'observations.txt',
 'rel_path': 'observations.txt',
 'size': 0,
 'type': 'file'}
✔ Validation successful!
```

For details on the fields available in each `file` dictionary, see the [dataclass attributes of the `FileMetadata` class](../../api/snapshot/#datajoint_file_validator.snapshot.FileMetadata).

!!! note "Tip: Debugging with `eval`"

    The `eval` constraint can be useful for debugging new rules.
    For example, we can use it to ensure that the `query` field works as expected:

    ```{.yaml linenums="60"}
    - id: new_rule_with_query
      query:
        type: file
        path: 'my_subdirectory/subject*.csv'
      eval: |
        def debug_query(files: List[Dict[str, Any]]) -> bool:
            print(f"Our query returned files:\n\n{pformat(files)}", file=sys.stderr)
            return True
    ```

    When we validate, we see all the files that match our query:

    ```console
    $ datajoint-file-validator validate $MY_FILESET_PATH my_type.yaml
    Our query returned files:

    [{'abs_path': '/path/to/my_fileset/my_subdirectory/subject2.csv',
      'atime_ns': 1705600299673026466,
      'ctime_ns': 1705600299673026466,
      'extension': '.csv',
      'last_modified': '2024-01-18T10:51:39.673027+00:00',
      'mtime_ns': 1705600299673026466,
      'name': 'subject2.csv',
      'path': 'my_subdirectory/subject2.csv',
      'rel_path': 'my_subdirectory/subject2.csv',
      'size': 0,
      'type': 'file'},
     {'abs_path': '/path/to/my_fileset/my_subdirectory/subject1.csv',
      'atime_ns': 1705600299673026466,
      'ctime_ns': 1705600299673026466,
      'extension': '.csv',
      'last_modified': '2024-01-18T10:51:39.673027+00:00',
      'mtime_ns': 1705600299673026466,
      'name': 'subject1.csv',
      'path': 'my_subdirectory/subject1.csv',
      'rel_path': 'my_subdirectory/subject1.csv',
      'size': 0,
      'type': 'file'}]
    ✔ Validation successful!
    ```

### 1.7.1. Best Practices

With the `eval` constraint, manifest authors have flexibility to write almost any rule they can think of.
But with great power comes great responsibility, so we recommend that you adhere to the following best practices:

- Use a built-in constraint if possible. Built-in constraints validate faster, and emit more informative error messages when validation fails.
- Avoid running complex or computationally intensive logic in `eval` functions. Fileset validation should be quick and easy to run. Instead, move complex logic to a separate script and use `datajoint-file-validator` as a dependency.
- Ensure that the code you write in `eval` is safe to run. Avoid fetching data from the internet or installing software in the `eval` function.
- If the function `print`s anything, ensure that it writes to `sys.stderr`, not the default `sts.stdout` buffer. You can achieve this by passing `file=sys.stderr` to the `print` function. This ensures that users can redirect [validation reports from `STDOUT` to file](1-validate.md#15-validate-the-fileset-using-the-cli) without corrupting the YAML or JSON formatted report.

## 1.8. Conclusion

In this section, we learned how to write a custom manifest that can be used to validate a fileset.
We encourage you to experiment with writing your own manifests, and consult the [manifest registry](registry/index.md) for examples and inspiration.
The complete manifest that we wrote in this section is shown below:


<details>
<summary> <code>my_type.yaml</code> </summary>

```{.yaml linenums="1"}
--8<-- "snippets/my_type.yaml"
```

</details>

## Next Steps

Now that you've written a custom manifest, you can publish it to the [manifest registry](registry/index.md) so that others can use or extend it.
See [part 3](3-publish.md) of this tutorial for more details.
