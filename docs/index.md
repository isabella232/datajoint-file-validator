# DataJoint File Validator

<p align="center">
<a href="https://github.com/ethho/datajoint-file-validator/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/ethho/datajoint-file-validator/workflows/Test/badge.svg" alt="Test">
</a>
<!-- <a href="https://github.com/ethho/datajoint-file-validator/actions?query=workflow%3APyPi" target="_blank">
    <img src="https://github.com/ethho/datajoint-file-validator/workflows/PyPi/badge.svg" alt="Publish">
</a> -->
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/ethho/datajoint-file-validator" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/ethho/datajoint-file-validator.svg" alt="Coverage">
</a>
<!-- <a href="https://pypi.org/project/datajoint-file-validator" target="_blank">
    <img src="https://img.shields.io/pypi/v/datajoint-file-validator?color=%2334D058&label=pypi%20package" alt="Package version">
</a> -->
</p>


The DataJoint File Validator is a framework for file validation.
It is designed to be used with [DataJoint](https://datajoint.com/docs) pipelines, but can be used independently.
The Python package `datajoint_file_validator` allows users to check if their files or filesets are of a certain **fileset type**; that is, if they conform to a set of rules and constraints defined in a **manifest** for that fileset type.
Through the [Python API](usage.md#validate-using-python-api) or the [command line interface (CLI)](usage.md#validate-using-the-command-line-interface-cli), users can validate files or filesets against a manifest and receive a report of any errors or warnings.

The DataJoint File Validator is designed to be extensible.
Users can define their own fileset types by [writing manifests](tutorial/2-manifest.md) that define rules and constraints for their custom fileset type.
Users are encouraged to share their manifests with the community by [contributing them to the Manifest Registry](contribute.md#contribute-a-manifest).
The Python package defines a [manifest language](src/manifest_schemas/latest.yaml) that aids in writing custom manifests.
