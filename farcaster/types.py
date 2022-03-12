from typing import NamedTuple

Cast = NamedTuple(
    "Cast",
    hash=str,
    content=str,
)

Caster = NamedTuple(
    "Caster",
    hash=str,
    display_name=str,
    activity_url=str,
)
