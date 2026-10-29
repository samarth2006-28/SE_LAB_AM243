import pytest
from blood_donation_screening import process_donor_cohort, verify_storage_centrifuge

# Example test case:
def test_single_accepted_donor():
    cohorts = [
        {
            "clinic_registered": True,
            "type": "standard",
            "fast_track": False,
            "donors": [{"age": 25, "weight_kg": 65, "hb": 14.0}]
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 450
    assert result["status"] == "ACCEPTED"

# TODO: Add test cases to achieve 90-100% on both Line and Branch coverage!