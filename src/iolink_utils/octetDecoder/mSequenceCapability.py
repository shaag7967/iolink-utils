from dataclasses import dataclass


@dataclass(frozen=True)
class MSequenceCapability:
    code: int

    @property
    def isdu_supported(self) -> bool:
        return bool(self.code & 0b00000001)

    @property
    def operate_code(self) -> int:
        return (self.code >> 1) & 0b111

    @property
    def preoperate_code(self) -> int:
        return (self.code >> 4) & 0b11

    def __repr__(self):
        return (f"MSequenceCapability("
                f"isdu={self.isdu_supported}, "
                f"operate={self.operate_code}, "
                f"preoperate={self.preoperate_code})")
