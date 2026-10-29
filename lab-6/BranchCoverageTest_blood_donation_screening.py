"""Branch coverage tests for blood_donation_screening.py.

Every decision point (if / elif / for) is driven down both its True and
False outcomes, plus boundary values for each threshold.
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


def donor(age=30, weight=70, hb=14.0):
    return {"age": age, "weight_kg": weight, "hb": hb}


# ---------- line 2: input validation (True / False) ----------

@pytest.mark.parametrize("cohorts, volume", [
    ("not a list", 450),        # not a list
    ({"a": 1}, 450),            # dict is not a list
    ([], 0),                    # volume == 0
    ([], -10),                  # volume < 0
])
def test_invalid_input_raises(cohorts, volume):
    with pytest.raises(ValueError):
        process_donor_cohort(cohorts, volume)


def test_empty_cohort_list_is_zero_yield():
    # line 8 loop not entered at all
    assert process_donor_cohort([], 450) == {"collected_ml": 0, "status": "ZERO_YIELD"}


# ---------- line 9: clinic_registered (True / False / missing key) ----------

def test_unregistered_cohort_skipped():
    cohorts = [make_cohort([donor()], registered=False)]
    assert process_donor_cohort(cohorts, 450)["status"] == "ZERO_YIELD"


def test_missing_registration_key_defaults_to_skipped():
    assert process_donor_cohort([{"donors": [donor()]}], 450)["status"] == "ZERO_YIELD"


def test_registered_and_unregistered_mixed():
    cohorts = [make_cohort([donor()], registered=False), make_cohort([donor()])]
    assert process_donor_cohort(cohorts, 450) == {"collected_ml": 450, "status": "ACCEPTED"}


def test_defaults_for_type_and_donors():
    # cohort without "type" or "donors" keys -> standard, empty donor list
    assert process_donor_cohort([{"clinic_registered": True}], 450)["status"] == "ZERO_YIELD"


# ---------- line 20: age / weight eligibility ----------

@pytest.mark.parametrize("age, weight", [(16, 70), (30, 49), (10, 30)])
def test_age_or_weight_deferral(age, weight):
    result = process_donor_cohort([make_cohort([donor(age=age, weight=weight)])], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_age_and_weight_boundaries_accepted():
    # age == 17 and weight == 50 are eligible
    result = process_donor_cohort([make_cohort([donor(age=17, weight=50)])], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_missing_donor_fields_default_to_deferral():
    assert process_donor_cohort([make_cohort([{}])], 450)["status"] == "ZERO_YIELD"


# ---------- lines 24 / 26 / 29: hemoglobin decisions ----------

def test_low_hb_standard_cohort_continues_with_next_donor():
    # hb < 12.5 in a standard cohort: branch 26 -> 15 (no reset, loop continues)
    cohorts = [make_cohort([donor(hb=12.0), donor(hb=14.0)])]
    assert process_donor_cohort(cohorts, 450) == {"collected_ml": 450, "status": "ACCEPTED"}


def test_low_hb_high_altitude_resets_and_stops_cohort():
    # hb < 12.5 in a high_altitude cohort: total reset and break
    cohorts = [make_cohort([donor(hb=14.0), donor(hb=11.0), donor(hb=14.0)],
                           cohort_type="high_altitude")]
    assert process_donor_cohort(cohorts, 450) == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_high_altitude_reset_wipes_previous_cohorts_too():
    cohorts = [make_cohort([donor()]),
               make_cohort([donor(hb=10.0)], cohort_type="high_altitude"),
               make_cohort([donor()])]
    assert process_donor_cohort(cohorts, 450) == {"collected_ml": 450, "status": "ACCEPTED"}


def test_high_altitude_with_healthy_donors_collects():
    cohorts = [make_cohort([donor(), donor()], cohort_type="high_altitude")]
    assert process_donor_cohort(cohorts, 450) == {"collected_ml": 900, "status": "ACCEPTED"}


def test_high_hb_deferred():
    cohorts = [make_cohort([donor(hb=18.1)])]
    assert process_donor_cohort(cohorts, 450) == {"collected_ml": 0, "status": "ZERO_YIELD"}


@pytest.mark.parametrize("hb", [12.5, 18.0])
def test_hb_boundaries_accepted(hb):
    assert process_donor_cohort([make_cohort([donor(hb=hb)])], 450)["collected_ml"] == 450


# ---------- line 35: fast_track (True / False) ----------

def test_fast_track_adds_bonus():
    cohorts = [make_cohort([donor()], fast_track=True)]
    assert process_donor_cohort(cohorts, 450) == {"collected_ml": 500, "status": "ACCEPTED"}


def test_fast_track_after_high_altitude_reset():
    cohorts = [make_cohort([donor(hb=11.0)], cohort_type="high_altitude", fast_track=True)]
    assert process_donor_cohort(cohorts, 450) == {"collected_ml": 50, "status": "ACCEPTED"}


# ---------- lines 38 / 40: final status ----------

def test_exactly_four_deferrals_is_not_high_deferral():
    donors = [donor(age=16)] * 4 + [donor()]
    assert process_donor_cohort([make_cohort(donors)], 450) == {"collected_ml": 450, "status": "ACCEPTED"}


def test_five_deferrals_is_high_deferral():
    donors = [donor(age=16), donor(weight=40), donor(hb=19.0), donor(hb=18.5), donor(hb=11.0), donor()]
    assert process_donor_cohort([make_cohort(donors)], 450) == {"collected_ml": 450, "status": "HIGH_DEFERRAL"}


def test_high_deferral_with_zero_collected():
    donors = [donor(age=16)] * 5
    assert process_donor_cohort([make_cohort(donors)], 450) == {"collected_ml": 0, "status": "HIGH_DEFERRAL"}


# ---------- verify_storage_centrifuge ----------

@pytest.mark.parametrize("runs", [[], None])
def test_centrifuge_no_data(runs):
    assert verify_storage_centrifuge(runs) == "NO_DATA"


def test_centrifuge_all_runs_stable():
    assert verify_storage_centrifuge([[3500, 3600], [3000, 3100]]) == "STABLE"


def test_centrifuge_empty_run_is_stable():
    assert verify_storage_centrifuge([[]]) == "STABLE"


def test_centrifuge_single_drop_then_recovery_is_stable():
    # drop streak reset by a good reading (line 57)
    assert verify_storage_centrifuge([[2900, 3200, 2900, 3200]]) == "STABLE"


def test_centrifuge_single_drop_at_end_is_stable():
    assert verify_storage_centrifuge([[3500, 2999]]) == "STABLE"


def test_centrifuge_two_consecutive_drops_abort():
    assert verify_storage_centrifuge([[3500, 2900, 2800]]) == "ABORT_SPIN"


def test_centrifuge_streak_resets_between_runs():
    # one drop at end of run 1 and one at start of run 2 are not consecutive
    assert verify_storage_centrifuge([[3500, 2900], [2900, 3500]]) == "STABLE"


def test_centrifuge_failure_in_later_run():
    assert verify_storage_centrifuge([[3500, 3600], [2000, 1000]]) == "ABORT_SPIN"
