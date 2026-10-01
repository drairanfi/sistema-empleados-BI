"""Turns a validated Excel file into Employee objects."""

from employee import Employee
from excel_validator import validate_excel


def _normalize_doc_number(value):
    # Excel stores numeric documents as floats (1076669247.0)
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def read_employees(path):
    rows = validate_excel(path)
    return [
        Employee(
            doc_type=str(doc_type).strip().upper(),
            doc_number=_normalize_doc_number(doc_number),
            salary=float(salary),
        )
        for doc_type, doc_number, salary, *_ in rows
    ]
