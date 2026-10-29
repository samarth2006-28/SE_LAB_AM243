def process_donor_cohort(cohorts, standard_volume_ml):
    if not isinstance(cohorts, list) or standard_volume_ml <= 0:
        raise ValueError("Invalid cohort list or volume")

    total_collected_ml = 0
    deferred_count = 0

    for cohort in cohorts:
        if not cohort.get("clinic_registered", False):
            continue

        cohort_type = cohort.get("type", "standard")
        donors = cohort.get("donors", [])

        for donor in donors:
            age = donor.get("age", 0)
            weight = donor.get("weight_kg", 0)
            hemoglobin = donor.get("hb", 0.0)

            if age < 17 or weight < 50:
                deferred_count += 1
                continue

            if hemoglobin < 12.5:
                deferred_count += 1
                if cohort_type == "high_altitude":
                    total_collected_ml = 0
                    break
            elif hemoglobin > 18.0:
                deferred_count += 1
                continue
            else:
                total_collected_ml += standard_volume_ml

        if cohort.get("fast_track", False):
            total_collected_ml += 50

    if deferred_count > 4:
        return {"collected_ml": total_collected_ml, "status": "HIGH_DEFERRAL"}
    if total_collected_ml == 0:
        return {"collected_ml": 0, "status": "ZERO_YIELD"}
    return {"collected_ml": total_collected_ml, "status": "ACCEPTED"}


def verify_storage_centrifuge(centrifuge_runs):
    if not centrifuge_runs:
        return "NO_DATA"

    for run in centrifuge_runs:
        rpm_drop_streak = 0
        for rpm in run:
            if rpm < 3000:
                rpm_drop_streak += 1
                if rpm_drop_streak >= 2:
                    return "ABORT_SPIN"
            else:
                rpm_drop_streak = 0
    return "STABLE"