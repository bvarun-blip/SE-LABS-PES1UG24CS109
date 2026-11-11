"""Validated daycare-fee processor used by Lab 7."""

INCLUDED_HOURS = {"infant": 20, "toddler": 25, "preschool": 30}


def _require_bool(value, name):
    if type(value) is not bool:
        raise TypeError(f"{name} must be a boolean")


def _require_integer(value, name, *, minimum=None):
    # bool is an int subclass, but it is never a valid count of hours/months.
    if type(value) is not int:
        raise TypeError(f"{name} must be an integer")
    if minimum is not None and value < minimum:
        raise ValueError(f"invalid {name}")


def extra_hours_fee(age_group, hours, has_sibling):
    """Return the fee for care beyond the included hours for an age group."""
    if not isinstance(age_group, str):
        raise TypeError("age_group must be a string")
    if age_group not in INCLUDED_HOURS:
        raise ValueError("unknown age group")
    _require_integer(hours, "hours", minimum=0)
    _require_bool(has_sibling, "has_sibling")

    included = INCLUDED_HOURS[age_group]
    if has_sibling and age_group != "infant":
        included += 5
    extra = max(0, hours - included)
    if extra == 0:
        return 0

    rate = 14 if age_group == "infant" else 9
    if extra > 20:
        rate += 5
        if age_group == "infant":
            rate += 3
    return extra * rate


def enrolment_allowed(age_months, vacancies, is_immunisation_pending):
    """Return whether a child meets the age and vacancy enrolment rules."""
    _require_integer(age_months, "age_months", minimum=0)
    _require_integer(vacancies, "vacancies", minimum=0)
    _require_bool(is_immunisation_pending, "is_immunisation_pending")

    if is_immunisation_pending:
        return age_months >= 12
    if age_months < 6:
        return False
    return vacancies >= 1


def pickup_status(minutes_left, is_aftercare, is_friday):
    """Classify pickup timing using the weekday and aftercare cutoffs."""
    _require_integer(minutes_left, "minutes_left")
    _require_bool(is_aftercare, "is_aftercare")
    _require_bool(is_friday, "is_friday")

    cutoff = 20 if is_aftercare else 10
    if is_friday:
        cutoff += 10
    if minutes_left >= cutoff:
        return "on_time"
    if minutes_left >= cutoff - 15:
        return "late"
    return "overdue"


def main():
    """Run a small, repeatable demonstration of the three app functions."""
    print("Daycare fee processor demo")
    fee = extra_hours_fee("toddler", 31, False)
    enrolled = enrolment_allowed(24, 2, False)
    status = pickup_status(19, True, False)
    print(f"Extra-hours fee (toddler, 31 hours, no sibling): ${fee}")
    print(f"Enrolment (24 months, 2 vacancies, no pending immunisation): {enrolled}")
    print(f"Pickup (19 minutes left, aftercare, weekday): {status}")


if __name__ == "__main__":
    main()
