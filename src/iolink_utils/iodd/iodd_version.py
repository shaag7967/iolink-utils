import re
from functools import total_ordering


@total_ordering
class Version:
    VERSION_PATTERN = re.compile(r"^V(\d+(?:\.\d+){1,7})$")

    def __init__(self, version_str: str):
        match = self.VERSION_PATTERN.match(version_str)
        if not match:
            raise ValueError(f"Invalid version string: {version_str}")
        self.parts = [int(p) for p in match.group(1).split(".")]

    def __eq__(self, other):
        return self.parts == other.parts

    def __lt__(self, other):
        max_len = max(len(self.parts), len(other.parts))
        padded_self = self.parts + [0] * (max_len - len(self.parts))
        padded_other = other.parts + [0] * (max_len - len(other.parts))
        return padded_self < padded_other

    def __repr__(self):
        return f"Version({'V' + '.'.join(map(str, self.parts))})"
