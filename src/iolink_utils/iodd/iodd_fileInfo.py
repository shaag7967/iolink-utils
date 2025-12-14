from typing import Optional
from datetime import date, datetime
from pathlib import Path
import re
from iolink_utils.utils.version import Version


class IoddFileInfo:
    # <vendor name>-<device name>-<release date>-IODD<schema version>.xml
    def __init__(self, filename: str):
        path = Path(filename).resolve()
        self.dirPath: str = str(path.parent)
        self.filename: str = str(path.name)
        self.fullPathFilename: str = str(path)
        self.fileExists: bool = path.is_file()
        self.sizeInBytes: int = path.stat().st_size if self.fileExists else 0
        self.date: Optional[date] = None
        self.schemaVersion: Version = Version()

        match = re.search(r"-(\d{8})-IODD(\d+(?:\.\d+)*)(?:-[a-z]{2})?\.xml", filename)
        if match:
            self.date = datetime.strptime(match.group(1), "%Y%m%d").date()
            self.schemaVersion = Version(match.group(2))

    def __str__(self):  # pragma: no cover
        return (
            f"IoddFileInfo("
            f"fullPathFilename={self.fullPathFilename}, "
            f"fileExists={self.fileExists}, "
            f"sizeInBytes={self.sizeInBytes}, "
            f"date={self.date}, "
            f"schemaVersion={self.schemaVersion}"
            f")"
        )
