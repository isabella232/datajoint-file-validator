from typing import List
import os.path
from .snapshot import FileMetadata, Snapshot
from wcmatch import glob

GLOB_FLAGS = glob.GLOBSTAR | glob.MARK | glob.FOLLOW


def find_matching_paths(filenames, patterns, flags=GLOB_FLAGS, **kw):
    return glob.globfilter(filenames, patterns, flags=flags, **kw)


def find_matching_files_gen(snapshot: Snapshot, patterns):
    filenames = [file.get("path") for file in snapshot]
    return (
        file
        for file in snapshot
        if file.get("path") in set(find_matching_paths(filenames, patterns))
    )


def find_matching_files(snapshot: Snapshot, patterns):
    return list(find_matching_files_gen(snapshot, patterns))
