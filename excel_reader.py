"""Turns an Excel file into Employee objects, skipping rows that cannot be used."""

from config import NOTIFY_DOC_TYPES
from employee import Employee
from excel_validator import normalize_doc_number, validate_excel, validate_row


def read_employees(path):
    """Returns (employees, warnings).

    The file may contain invalid rows, repeated document numbers or notified
    types (e.g. PAS). Those rows are skipped and described in warnings so the
    application keeps working with the valid employees only.
    """
    rows = validate_excel(path)
    employees = []
    warnings = []
    seen = {}

    for index, row in rows:
        problems = validate_row(index, row)
        if problems:
            warnings.extend(problems)
            continue

        doc_type = str(row[0]).strip().upper()
        doc_number = normalize_doc_number(row[1])

        if doc_type in NOTIFY_DOC_TYPES:
            warnings.append(f"Fila {index}: TIPODOC '{doc_type}' ignorado.")
            continue

        if doc_number in seen:
            warnings.append(
                f"Fila {index}: NRODOCUMENTO {doc_number} repetido "
                f"(fila {seen[doc_number]}); ignorado."
            )
            continue

        seen[doc_number] = index
        employees.append(
            Employee(doc_type=doc_type, doc_number=doc_number, salary=float(row[2]))
        )

    return employees, warnings
