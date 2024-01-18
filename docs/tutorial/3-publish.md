# 3. Publish a Custom Manifest to the Registry

If you've been following along the tutorial, you now have a manifest file for your custom fileset type `my_type`.
Please see the [previous section](./2-manifest.md) if you have not yet created a custom manifest file.
You can now use your custom manifest to validate filesets, and you might want to share it with others (say, in your research group or with collaborators).
In this section, we'll guide you through the process of publishing your manifest to the registry.

## 3.1. Using GitHub

Currently, the only supported way to publish a manifest is to add it to the standard library, which is distributed with the [Python package](https://github.com/ethho/datajoint-file-validator.git).

### 3.1.1. Fork the Repository

First, create a fork of the DataJoint File Validator GitHub repository: [`https://github.com/ethho/datajoint-file-validator.git`](https://github.com/ethho/datajoint-file-validator.git):

![Fork the repository](../images/fork_repo.png)

### 3.1.2. Clone the Fork

Next, clone your fork to your local machine:

<!-- termynal -->

```console
$ export GITHUB_USERNAME="<your GitHub username>"
$ git clone https://github.com/${GITHUB_USERNAME}/datajoint-file-validator.git
---> 100%
$ cd datajoint-file-validator
$ git switch -c main
```

### 3.1.3. Push Your Manifest File to Your Fork

Now, create a new directory in the standard library directory that is named after your fileset type.
Ensure that the name of your fileset type is unique across all manifests.
Since our example fileset type is called `my_type`, we will create a directory called `my_type`:

<!-- termynal -->

```console
$ mkdir datajoint_file_validator/manifests/my_type
```

Copy your manifest file to this new directory, with a file name that matches the `version` of the manifest file.
The version of our manifest is `0.1.0`, so we will copy the manifest file to `datajoint_file_validator/manifests/my_type/v0.1.0.yaml`.
We should also create a **manifest reference file** called `default.yaml` that **includes** the `v0.1.0.yaml` file.
This reference file should:

1. Be named `default.yaml`
2. Contain only an `!include` tag (and optional comments), and
3. Reside in the same directory as `v0.1.0.yaml`.

```yaml
# default.yaml
!include: v0.1.0.yaml
```

We can copy our manifest file and create the manifest reference file with the following commands:

<!-- termynal -->

```console
$ cp my_type.yaml datajoint_file_validator/manifests/my_type/v0.1.0.yaml
$ echo '!include: v0.1.0.yaml' > datajoint_file_validator/manifests/my_type/default.yaml
```

The `default.yaml` file is necessary in order for the Python package to recognize our new manifest file.
It also makes our new manifest discoverable using the [`list_manifests`](./1-validate.md#16-list-available-manifests) function.
When we want to update our manifest file in the future, instead of changing the `v0.1.0.yaml` file, we should create a new manifest file with a new version number (e.g., `v0.1.1.yaml`), and update the `default.yaml` file to include the new manifest file.

!!! note

	A manifest reference is similar to a symbolic link in Unix systems, but there are [technical limitations](https://github.com/ethho/datajoint-file-validator/pull/12) that prevent us from using symbolic links.

We can now commit and push changes to our fork:

<!-- termynal -->

```console
$ git add datajoint_file_validator/manifests/my_type/
$ git commit -m "Add manifest for my_type v0.1.0"
$ git push origin main
```

### 3.1.4. Create a Pull Request Against the Main Repository

Finally, create a pull request against the `main` branch of the main repository by following this link:

1. [Click here to create a pull request for a new manifest](https://github.com/ethho/datajoint-file-validator/compare/main?template=new_manifest.md&labels=new-manifest,manifest&title=New+Manifest&assignees=ethho&is_cross_repo=1)
2. Click "compare across forks" and select your fork and `main` branch (or whichever branch you pushed to)
3. Click "Create a Pull Request"
