"""Manage gym membership registration and renewal operations."""

import hashlib
import secrets
from typing import Any, Dict, List, Optional

MEMBERS: Dict[str, Dict[str, Any]] = {
    "M01": {"name": "Alex", "plan": "Gold", "months_left": 6, "fee": 600.0},
    "M02": {"name": "Brooke", "plan": "Silver", "months_left": 1, "fee": 350.0},
    "M03": {"name": "Chris", "plan": "Platinum", "months_left": 12, "fee": 1000.0},
}


def register_member(
    member_id: str,
    name: str,
    plan: str,
    months: int,
    member_log: Optional[List[str]] = None,
) -> bool:
    """Register a new member and optionally record the operation."""
    if member_log is None:
        member_log = []
    if member_id in MEMBERS or months <= 0:
        return False
    MEMBERS[member_id] = {
        "name": name,
        "plan": plan,
        "months_left": months,
        "fee": 50.0 * months,
    }
    member_log.append(f"Registered {member_id} for {months} months")
    return True


def cancel_membership(member_id: str) -> bool:
    """Remove a member; return False when the member does not exist."""
    return MEMBERS.pop(member_id, None) is not None


def check_membership_status(member_id: str) -> bool:
    """Return whether a member has an active membership."""
    member = MEMBERS.get(member_id)
    return member is not None and member["months_left"] > 0


def calculate_renewal_rate(member_id: str, discount_rate: float) -> float:
    """Calculate a renewal fee using a discount between 0 and 1."""
    if not 0 <= discount_rate <= 1:
        raise ValueError("Discount rate must be between 0 and 1.")
    member = MEMBERS.get(member_id)
    if member is None:
        raise KeyError(f"Unknown member ID: {member_id}")
    return member["fee"] * (1 - discount_rate)


def generate_member_hash(member_id: str) -> str:
    """Return a SHA-256 digest for a member identifier."""
    return hashlib.sha256(member_id.encode("utf-8")).hexdigest()


def generate_locker_pin() -> int:
    """Generate a secure four-digit locker PIN."""
    return secrets.randbelow(9000) + 1000


def export_member_roster(filename: str = "gym_roster.txt") -> None:
    """Export the current member roster as text."""
    with open(filename, "w", encoding="utf-8") as roster_file:
        roster_file.write(str(MEMBERS))
    print(f"Roster exported to: {filename}")


def get_active_summary(member_records: Dict[str, Dict[str, Any]]) -> int:
    """Count members whose memberships have not expired."""
    return sum(
        1 for details in member_records.values() if details["months_left"] > 0
    )


def main() -> None:
    """Run a small demonstration of the gym membership functions."""
    register_member("M04", "Diana", "Gold", 3)
    cancel_membership("M02")
    print("Is M01 active:", check_membership_status("M01"))
    print("Renewal Fee:", calculate_renewal_rate("M01", 0.15))
    print("Member Hash:", generate_member_hash("M01"))
    print("Locker PIN:", generate_locker_pin())
    export_member_roster()
    print("Active count:", get_active_summary(MEMBERS))


if __name__ == "__main__":
    main()
