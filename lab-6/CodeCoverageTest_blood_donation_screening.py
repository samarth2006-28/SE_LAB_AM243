"""Code (line) coverage tests for blood_donation_screening.py.

Each test is aimed at executing statements that the starter test never
reached, so that every line of the module runs at least once.
"""
import pytest
from blood_donation_screening import process_donor_cohort, verify_storage_centrifuge


def make_cohort(donors, cohort_type="standard", registered=True, fast_track=False):
    return {
        "clinic_registered": registered,
        "type": cohort_type,
        "fast_track": fast_track,
        "donors": donors,
    }


# ---------- process_donor_cohort ----------

def test_single_accepted_donor():
    result = process_donor_cohort([make_cohort([{"age": 25, "weight_kg": 65, "hb": 14.0}])], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_invalid_input_raises():
    # line 3: raise ValueError
    with pytest.raises(ValueError):
        process_donor_cohort("not a list", 450)


def test_unregistered_cohort_skipped_gives_zero_yield():
    # line 10 (continue) and line 41 (ZERO_YIELD)
    cohorts = [make_cohort([{"age": 30, "weight_kg": 70, "hb": 14.0}], registered=False)]
    assert process_donor_cohort(cohorts, 450) == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_high_altitude_low_hb_resets_collection_and_fast_track():
    # lines 25-28 (low hb in high_altitude cohort) and line 36 (fast_track bonus)
    donors = [
        {"age": 30, "weight_kg": 70, "hb": 14.0},
        {"age": 30, "weight_kg": 70, "hb": 11.0},
    ]
    cohorts = [make_cohort(donors, cohort_type="high_altitude", fast_track=True)]
    assert process_donor_cohort(cohorts, 450) == {"collected_ml": 50, "status": "ACCEPTED"}


def test_many_deferrals_gives_high_deferral():
    # lines 21-22 (age/weight deferral), 30-31 (hb too high), 39 (HIGH_DEFERRAL)
    donors = [
        {"age": 16, "weight_kg": 70, "hb": 14.0},
        {"age": 30, "weight_kg": 45, "hb": 14.0},
        {"age": 30, "weight_kg": 70, "hb": 18.5},
        {"age": 30, "weight_kg": 70, "hb": 19.0},
        {"age": 15, "weight_kg": 40, "hb": 14.0},
        {"age": 30, "weight_kg": 70, "hb": 14.0},
    ]
    result = process_donor_cohort([make_cohort(donors)], 450)
    assert result == {"collected_ml": 450, "status": "HIGH_DEFERRAL"}


# ---------- verify_storage_centrifuge ----------

def test_centrifuge_no_data():
    # lines 46-47
    assert verify_storage_centrifuge([]) == "NO_DATA"


def test_centrifuge_two_consecutive_drops_aborts():
    # lines 49-55 including the reset on line 57
    assert verify_storage_centrifuge([[3500, 2900, 3200, 2800, 2700]]) == "ABORT_SPIN"


def test_centrifuge_stable():
    # line 58
    assert verify_storage_centrifuge([[3500, 3600, 3400]]) == "STABLE"
