import pytest
from daycare_fees import extra_hours_fee, enrolment_allowed, pickup_status


@pytest.mark.parametrize(
    "age_group,hours,has_sibling,expected",
    [
        ("infant", 20, False, 0),       # included hours boundary
        ("infant", 21, False, 14),      # infant base rate
        ("toddler", 25, False, 0),      # included hours boundary
        ("toddler", 31, False, 54),     # non-infant base rate
        ("preschool", 35, True, 0),     # sibling adds 5 included hours
        ("toddler", 51, True, 294),    # more than 20 extra hours, non-infant rate increase
        ("infant", 42, True, 484),      # infant rate increase; sibling does not add hours
    ],
)
def test_extra_hours_fee_valid_cases(age_group, hours, has_sibling, expected):
    assert extra_hours_fee(age_group, hours, has_sibling) == expected


def test_extra_hours_fee_unknown_age_group():
    with pytest.raises(ValueError, match="unknown age group"):
        extra_hours_fee("school_age", 10, False)


def test_extra_hours_fee_negative_hours():
    with pytest.raises(ValueError, match="invalid hours"):
        extra_hours_fee("toddler", -1, False)


@pytest.mark.parametrize(
    "age_months,vacancies,pending,expected",
    [
        (12, 0, True, True),   # pending immunisation, age meets threshold
        (11, 5, True, False),  # pending immunisation, too young
        (5, 5, False, False),  # below minimum age
        (6, 1, False, True),   # minimum age and vacancy available
        (6, 0, False, False),  # no vacancies
    ],
)
def test_enrolment_allowed_cases(age_months, vacancies, pending, expected):
    assert enrolment_allowed(age_months, vacancies, pending) is expected


@pytest.mark.parametrize(
    "minutes_left,is_aftercare,is_friday,expected",
    [
        (20, True, False, "on_time"),
        (19, True, False, "late"),
        (4, True, False, "overdue"),
        (10, False, False, "on_time"),
        (9, False, False, "late"),
        (-6, False, False, "overdue"),
        (30, True, True, "on_time"),
        (20, True, True, "late"),
        (14, True, True, "overdue"),
        (20, False, True, "on_time"),
        (10, False, True, "late"),
    ],
)
def test_pickup_status_cases(minutes_left, is_aftercare, is_friday, expected):
    assert pickup_status(minutes_left, is_aftercare, is_friday) == expected
