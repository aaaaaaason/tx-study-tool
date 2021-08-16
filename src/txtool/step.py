"""
Define object representation of each database execution step.
"""
import dataclasses


@dataclasses.dataclass
class Step:
    """Represents a step on database operation."""
    _session_id: int
    _statement: str

    @property
    def session_id(self) -> int:
        return self._session_id

    @property
    def statement(self) -> str:
        return self._statement.replace('\n', '')
