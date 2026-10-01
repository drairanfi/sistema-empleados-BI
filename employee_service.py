"""Business operations over the list of employees (one function per menu option)."""


def list_employees(employees):
    return list(employees)


def search_employee(employees, doc_number, doc_type=None):
    """Returns every match: the same number can exist under different doc types."""
    doc_number = str(doc_number).strip()
    return [
        e
        for e in employees
        if e.doc_number == doc_number and (doc_type is None or e.doc_type == doc_type)
    ]


def total_salaries(employees):
    return sum(e.salary for e in employees)


def average_salary(employees):
    if not employees:
        return 0.0
    return total_salaries(employees) / len(employees)


def highest_paid_employees(employees):
    """Returns all employees tied for the highest salary."""
    if not employees:
        return []
    top = max(e.salary for e in employees)
    return [e for e in employees if e.salary == top]


def employees_by_salary(employees, min_salary=None, max_salary=None, descending=True):
    """Filters by an optional salary range and sorts by salary."""
    filtered = [
        e
        for e in employees
        if (min_salary is None or e.salary >= min_salary)
        and (max_salary is None or e.salary <= max_salary)
    ]
    return sorted(filtered, key=lambda e: e.salary, reverse=descending)
