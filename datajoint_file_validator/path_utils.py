import fnmatch
from typing import List
import glob
import os.path
from itertools import product
from .snapshot import FileMetadata, Snapshot


# Cross-Python dictionary views on the keys
if hasattr(dict, "viewkeys"):
    # Python 2
    def _viewkeys(d):
        return d.viewkeys()

else:
    # Python 3
    def _viewkeys(d):
        return d.keys()


def _in_trie(trie, path):
    """Determine if path is completely in trie"""
    current = trie
    for elem in path:
        try:
            current = current[elem]
        except KeyError:
            return False
    return None in current


def find_matching_paths_generator(paths, pattern):
    """
    Produce a list of paths that match the pattern.
    ---

    paths: list of str
        List of paths to search.
    pattern: str
        Pattern to match.

    Adapted from
    https://stackoverflow.com/questions/27726545/python-glob-but-against-a-list-of-strings-rather-than-the-filesystem
    """
    if os.altsep:  # normalise
        pattern = pattern.replace(os.altsep, os.sep)
    pattern = pattern.split(os.sep)

    # build a trie out of path elements; efficiently search on prefixes
    path_trie = {}
    for path in paths:
        if os.altsep:  # normalise
            path = path.replace(os.altsep, os.sep)
        _, path = os.path.splitdrive(path)
        elems = path.split(os.sep)
        current = path_trie
        for elem in elems:
            current = current.setdefault(elem, {})
        current.setdefault(None, None)  # sentinel

    matching = []

    current_level = [path_trie]
    for subpattern in pattern:
        if not glob.has_magic(subpattern):
            # plain element, element must be in the trie or there are
            # 0 matches
            if not any(subpattern in d for d in current_level):
                return []
            matching.append([subpattern])
            current_level = [d[subpattern] for d in current_level if subpattern in d]
        else:
            # match all next levels in the trie that match the pattern
            matched_names = fnmatch.filter(
                {k for d in current_level for k in d}, subpattern
            )
            if not matched_names:
                # nothing found
                return []
            matching.append(matched_names)
            current_level = [
                d[n] for d in current_level for n in _viewkeys(d) & set(matched_names)
            ]

    return (os.sep.join(p) for p in product(*matching) if _in_trie(path_trie, p))


def find_matching_paths(paths, pattern) -> List:
    """
    Produce a list of paths that match the pattern.
    ---

    paths: list of str
        List of paths to search.
    pattern: str
        Pattern to match.
    """
    return list(find_matching_paths_generator(paths, pattern))


def find_matching_files(snapshot: Snapshot, pattern: str):
    paths = [file["path"] for file in snapshot]
    path_matches = find_matching_paths_generator(paths, pattern)
    path_matches = [os.path.normpath(path) for path in path_matches]
    return [file for file in snapshot if os.path.normpath(file["path"]) in path_matches]
