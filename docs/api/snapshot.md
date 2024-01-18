# Snapshot Module

::: datajoint_file_validator.snapshot.Snapshot
    handler: python
    options:
      show_root_heading: true

::: datajoint_file_validator.snapshot.S3URI
    handler: python
    options:
      show_root_heading: true

::: datajoint_file_validator.snapshot.PathLike
    handler: python
    options:
      show_root_heading: true

::: datajoint_file_validator.snapshot.create_snapshot
    handler: python
    options:
      show_root_heading: true
      show_source: true

::: datajoint_file_validator.snapshot.FileMetadata
    handler: python
    options:
      members:
        - from_path
        - to_iso_8601
        - asdict
      show_root_heading: true
      show_source: true

