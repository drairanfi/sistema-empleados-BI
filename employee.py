"""Domain model."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Employee:
    doc_type: str
    doc_number: str
    salary: float
