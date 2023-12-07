from dataclasses import dataclass


@dataclass
class Constraint:
    """A single constraint that evaluates True or False for a fileset."""
    pass


@dataclass
class CountMinConstraint(Constraint):
    """Constraint for `count_min`."""
    val: int


CONSTRAINT_MAP = {
    "count_min": CountMinConstraint,
}
