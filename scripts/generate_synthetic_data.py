from __future__ import annotations

import csv
import random
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

from faker import Faker

SEED = 20260417
PATIENT_COUNT = 4000
FACILITY_COUNT = 25
ENCOUNTER_COUNT = 10000
DATE_START = date(2024, 1, 1)
DATE_END = date(2025, 12, 31)
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "seeds" / "raw"

faker = Faker("id_ID")
random.seed(SEED)
Faker.seed(SEED)


DIAGNOSIS_CATALOG = [
    ("E11.00", "Type 2 diabetes mellitus", "diabetes"),
    ("E11.01", "Type 2 diabetes mellitus with neuropathy", "diabetes"),
    ("E11.02", "Type 2 diabetes mellitus with nephropathy", "diabetes"),
    ("E11.03", "Type 2 diabetes mellitus with ophthalmic complication", "diabetes"),
    ("E10.10", "Type 1 diabetes mellitus", "diabetes"),
    ("R73.90", "Abnormal blood glucose", "diabetes"),
    ("I10.00", "Essential hypertension", "hypertension"),
    ("I11.90", "Hypertensive heart disease", "hypertension"),
    ("I12.90", "Hypertensive kidney disease", "hypertension"),
    ("I15.80", "Secondary hypertension", "hypertension"),
    ("R03.00", "Elevated blood pressure", "hypertension"),
    ("O13.90", "Gestational hypertension", "hypertension"),
    ("A15.00", "Pulmonary tuberculosis", "tuberculosis"),
    ("A16.20", "Tuberculosis of lung without confirmation", "tuberculosis"),
    ("A18.10", "Tuberculosis of genitourinary system", "tuberculosis"),
    ("Z20.10", "Contact with tuberculosis", "tuberculosis"),
    ("R76.10", "Abnormal tuberculosis test", "tuberculosis"),
    ("Z86.11", "History of tuberculosis", "tuberculosis"),
    ("J18.90", "Pneumonia, unspecified organism", "respiratory infection"),
    ("J06.90", "Acute upper respiratory infection", "respiratory infection"),
    ("J20.90", "Acute bronchitis", "respiratory infection"),
    ("J22.00", "Unspecified acute lower respiratory infection", "respiratory infection"),
    ("U07.10", "COVID-19", "respiratory infection"),
    ("J12.90", "Viral pneumonia", "respiratory infection"),
    ("O80.00", "Single spontaneous delivery", "maternal/child"),
    ("O82.00", "Delivery by caesarean section", "maternal/child"),
    ("Z34.90", "Normal pregnancy supervision", "maternal/child"),
    ("P07.30", "Preterm newborn", "maternal/child"),
    ("P59.90", "Neonatal jaundice", "maternal/child"),
    ("Z38.00", "Single liveborn infant", "maternal/child"),
    ("I21.90", "Acute myocardial infarction", "cardiovascular"),
    ("I25.10", "Atherosclerotic heart disease", "cardiovascular"),
    ("I50.90", "Heart failure", "cardiovascular"),
    ("I63.90", "Cerebral infarction", "cardiovascular"),
    ("I48.90", "Atrial fibrillation", "cardiovascular"),
    ("R07.90", "Chest pain", "cardiovascular"),
    ("N18.90", "Chronic kidney disease", "renal"),
    ("N17.90", "Acute kidney failure", "renal"),
    ("N39.00", "Urinary tract infection", "renal"),
    ("N20.00", "Kidney stone", "renal"),
    ("R94.40", "Abnormal kidney function study", "renal"),
    ("N19.00", "Unspecified kidney failure", "renal"),
    ("K29.70", "Gastritis", "gastrointestinal"),
    ("K52.90", "Noninfective gastroenteritis", "gastrointestinal"),
    ("K80.20", "Calculus of gallbladder", "gastrointestinal"),
    ("K35.80", "Acute appendicitis", "gastrointestinal"),
    ("K21.90", "Gastro-oesophageal reflux disease", "gastrointestinal"),
    ("R10.90", "Abdominal pain", "gastrointestinal"),
    ("K74.60", "Liver fibrosis and cirrhosis", "gastrointestinal"),
    ("B18.10", "Chronic viral hepatitis B", "gastrointestinal"),
]

FACILITY_TYPES = [
    "Rumah Sakit Umum",
    "Rumah Sakit Khusus",
    "Puskesmas",
    "Klinik",
    "Laboratorium",
]

LOCATION_PAIRS = [
    ("Jakarta Selatan", "DKI Jakarta"),
    ("Jakarta Timur", "DKI Jakarta"),
    ("Bandung", "Jawa Barat"),
    ("Bekasi", "Jawa Barat"),
    ("Bogor", "Jawa Barat"),
    ("Surabaya", "Jawa Timur"),
    ("Malang", "Jawa Timur"),
    ("Semarang", "Jawa Tengah"),
    ("Yogyakarta", "DI Yogyakarta"),
    ("Solo", "Jawa Tengah"),
    ("Denpasar", "Bali"),
    ("Makassar", "Sulawesi Selatan"),
    ("Medan", "Sumatera Utara"),
    ("Palembang", "Sumatera Selatan"),
    ("Balikpapan", "Kalimantan Timur"),
]

OWNERSHIP_TYPES = ["Pemerintah", "Swasta", "BUMN"]
PAYER_TYPES = ["JKN PBI", "JKN Mandiri", "Asuransi Swasta", "Umum"]
CLASS_OF_CARE = ["Kelas 1", "Kelas 2", "Kelas 3", "Rawat Jalan"]

GROUP_WEIGHTS = {
    "diabetes": 0.16,
    "hypertension": 0.16,
    "tuberculosis": 0.08,
    "respiratory infection": 0.18,
    "maternal/child": 0.10,
    "cardiovascular": 0.13,
    "renal": 0.09,
    "gastrointestinal": 0.10,
}

GROUP_TO_DIAGNOSES: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
for diagnosis in DIAGNOSIS_CATALOG:
    GROUP_TO_DIAGNOSES[diagnosis[2]].append(diagnosis)


def daterange_days() -> int:
    return (DATE_END - DATE_START).days


def random_date(start: date, end: date) -> date:
    return start + timedelta(days=random.randint(0, (end - start).days))


def build_facilities() -> list[dict[str, str | int]]:
    facilities = []
    location_cycle = LOCATION_PAIRS * 2
    type_prefix = {
        "Rumah Sakit Umum": "RSU",
        "Rumah Sakit Khusus": "RSK",
        "Puskesmas": "PKM",
        "Klinik": "KLN",
        "Laboratorium": "LAB",
    }
    for idx in range(FACILITY_COUNT):
        facility_type = FACILITY_TYPES[idx // 5]
        city, province = location_cycle[idx]
        facilities.append(
            {
                "facility_id": f"FAC-{idx + 1:03d}",
                "facility_name": f"{type_prefix[facility_type]} {faker.last_name()} {city}",
                "facility_type": facility_type,
                "city": city,
                "province": province,
                "ownership_type": random.choice(OWNERSHIP_TYPES),
            }
        )
    return facilities


def build_patients() -> list[dict[str, str]]:
    patients = []
    for idx in range(PATIENT_COUNT):
        city, province = random.choice(LOCATION_PAIRS)
        birth_start = date(1945, 1, 1)
        birth_end = date(2010, 12, 31)
        birth_date = random_date(birth_start, birth_end)
        patients.append(
            {
                "patient_id": f"PAT-{idx + 1:05d}",
                "gender": random.choices(["L", "P"], weights=[0.47, 0.53], k=1)[0],
                "birth_date": birth_date.isoformat(),
                "city": city,
                "province": province,
                "insurance_class": random.choices(
                    ["Kelas 1", "Kelas 2", "Kelas 3"], weights=[0.18, 0.31, 0.51], k=1
                )[0],
                "registered_at": random_date(date(2023, 1, 1), date(2025, 6, 30)).isoformat(),
            }
        )
    return patients


def encounter_count_distribution() -> list[int]:
    counts = [1] * PATIENT_COUNT
    remaining = ENCOUNTER_COUNT - PATIENT_COUNT
    while remaining > 0:
        idx = random.randrange(PATIENT_COUNT)
        if counts[idx] < 5:
            counts[idx] += 1
            remaining -= 1
    return counts


def encounter_gap_days() -> int:
    if random.random() < 0.35:
        return random.randint(7, 30)
    return random.randint(31, 150)


def diagnosis_for_group(group: str) -> tuple[str, str, str]:
    return random.choice(GROUP_TO_DIAGNOSES[group])


def weighted_group() -> str:
    groups = list(GROUP_WEIGHTS.keys())
    weights = list(GROUP_WEIGHTS.values())
    return random.choices(groups, weights=weights, k=1)[0]


def facility_pool(facilities: list[dict[str, str | int]], group: str) -> list[dict[str, str | int]]:
    if group == "maternal/child":
        valid = {"Rumah Sakit Umum", "Rumah Sakit Khusus", "Puskesmas", "Klinik"}
    elif group == "tuberculosis":
        valid = {"Rumah Sakit Umum", "Puskesmas", "Klinik", "Laboratorium"}
    elif group in {"diabetes", "hypertension"}:
        valid = {"Rumah Sakit Umum", "Puskesmas", "Klinik", "Laboratorium"}
    else:
        valid = {"Rumah Sakit Umum", "Rumah Sakit Khusus", "Klinik", "Puskesmas"}
    return [facility for facility in facilities if facility["facility_type"] in valid]


def length_of_stay_for_type(facility_type: str, group: str) -> int:
    if facility_type == "Laboratorium":
        return 0
    if facility_type == "Puskesmas":
        return random.choices([0, 1, 2], weights=[0.7, 0.2, 0.1], k=1)[0]
    if facility_type == "Klinik":
        return random.choices([0, 1, 2, 3], weights=[0.55, 0.25, 0.15, 0.05], k=1)[0]
    if facility_type == "Rumah Sakit Khusus":
        if group == "maternal/child":
            return random.randint(2, 6)
        return random.randint(1, 8)
    if group in {"cardiovascular", "renal"}:
        return random.randint(2, 8)
    return random.randint(1, 6)


def encounter_cost_for_type(facility_type: str, group: str, los: int) -> int:
    base = {
        "Laboratorium": 150_000,
        "Puskesmas": 250_000,
        "Klinik": 450_000,
        "Rumah Sakit Umum": 1_400_000,
        "Rumah Sakit Khusus": 1_800_000,
    }[facility_type]
    group_uplift = {
        "diabetes": 180_000,
        "hypertension": 120_000,
        "tuberculosis": 250_000,
        "respiratory infection": 200_000,
        "maternal/child": 420_000,
        "cardiovascular": 600_000,
        "renal": 520_000,
        "gastrointestinal": 240_000,
    }[group]
    stay_cost = los * random.randint(175_000, 650_000)
    noise = random.randint(-50_000, 250_000)
    return max(125_000, base + group_uplift + stay_cost + noise)


def build_encounters_and_diagnoses(
    patients: list[dict[str, str]], facilities: list[dict[str, str | int]]
) -> tuple[list[dict[str, str | int]], list[dict[str, str | int]]]:
    counts = encounter_count_distribution()
    encounters: list[dict[str, str | int]] = []
    diagnoses: list[dict[str, str | int]] = []
    encounter_id = 1
    diagnosis_id = 1

    patient_by_id = {patient["patient_id"]: patient for patient in patients}

    for patient_idx, patient in enumerate(patients):
        count = counts[patient_idx]
        gaps = [encounter_gap_days() for _ in range(max(0, count - 1))]
        total_gap_days = sum(gaps) + count * 5
        latest_start_offset = max(0, daterange_days() - total_gap_days)
        current_admission = DATE_START + timedelta(days=random.randint(0, latest_start_offset))

        for visit_idx in range(count):
            diagnosis_group = weighted_group()
            primary_code, primary_name, primary_group = diagnosis_for_group(diagnosis_group)
            facility = random.choice(facility_pool(facilities, primary_group))
            facility_type = str(facility["facility_type"])
            los = length_of_stay_for_type(facility_type, primary_group)
            discharge_date = min(current_admission + timedelta(days=los), DATE_END)
            encounter_cost = encounter_cost_for_type(facility_type, primary_group, los)
            payer_type = random.choices(PAYER_TYPES, weights=[0.34, 0.40, 0.11, 0.15], k=1)[0]
            class_of_care = (
                "Rawat Jalan"
                if los == 0
                else random.choices(CLASS_OF_CARE[:3], weights=[0.18, 0.31, 0.51], k=1)[0]
            )

            encounter = {
                "encounter_id": f"ENC-{encounter_id:06d}",
                "patient_id": patient["patient_id"],
                "facility_id": facility["facility_id"],
                "admission_date": current_admission.isoformat(),
                "discharge_date": discharge_date.isoformat(),
                "length_of_stay": los,
                "encounter_cost": encounter_cost,
                "payer_type": payer_type,
                "class_of_care": class_of_care,
            }
            encounters.append(encounter)

            primary_event_date = current_admission + timedelta(days=random.randint(0, max(los, 0)))
            diagnoses.append(
                {
                    "diagnosis_event_id": f"DGX-{diagnosis_id:07d}",
                    "encounter_id": encounter["encounter_id"],
                    "diagnosis_code": primary_code,
                    "diagnosis_name": primary_name,
                    "diagnosis_group": primary_group,
                    "diagnosis_type": "primary",
                    "diagnosis_event_date": primary_event_date.isoformat(),
                }
            )
            diagnosis_id += 1

            secondary_count = random.choices([0, 1, 2], weights=[0.38, 0.42, 0.20], k=1)[0]
            used_codes = {primary_code}
            for _ in range(secondary_count):
                secondary_group = weighted_group()
                secondary_code, secondary_name, secondary_group = diagnosis_for_group(secondary_group)
                if secondary_code in used_codes:
                    continue
                used_codes.add(secondary_code)
                secondary_event_date = current_admission + timedelta(days=random.randint(0, max(los, 0)))
                diagnoses.append(
                    {
                        "diagnosis_event_id": f"DGX-{diagnosis_id:07d}",
                        "encounter_id": encounter["encounter_id"],
                        "diagnosis_code": secondary_code,
                        "diagnosis_name": secondary_name,
                        "diagnosis_group": secondary_group,
                        "diagnosis_type": "secondary",
                        "diagnosis_event_date": secondary_event_date.isoformat(),
                    }
                )
                diagnosis_id += 1

            encounter_id += 1
            if visit_idx < count - 1:
                current_admission = discharge_date + timedelta(days=gaps[visit_idx])

    encounters.sort(key=lambda row: (row["admission_date"], row["encounter_id"]))
    diagnoses.sort(key=lambda row: (row["diagnosis_event_date"], row["diagnosis_event_id"]))

    encounter_ids = {row["encounter_id"] for row in encounters}
    diagnosis_encounters = {row["encounter_id"] for row in diagnoses}
    if encounter_ids != diagnosis_encounters:
        missing = encounter_ids - diagnosis_encounters
        raise ValueError(f"Every encounter must have a diagnosis. Missing: {sorted(missing)[:5]}")

    if len(encounters) != ENCOUNTER_COUNT:
        raise ValueError(f"Expected {ENCOUNTER_COUNT} encounters, got {len(encounters)}")

    if len({row['diagnosis_code'] for row in diagnoses}) != len(DIAGNOSIS_CATALOG):
        raise ValueError("Generated diagnoses did not cover the full 50-code catalog")

    return encounters, diagnoses


def write_csv(path: Path, rows: list[dict[str, str | int]]) -> None:
    if not rows:
        raise ValueError(f"No rows provided for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    facilities = build_facilities()
    patients = build_patients()
    encounters, diagnoses = build_encounters_and_diagnoses(patients, facilities)

    write_csv(OUTPUT_DIR / "raw_facility.csv", facilities)
    write_csv(OUTPUT_DIR / "raw_patient.csv", patients)
    write_csv(OUTPUT_DIR / "raw_encounter.csv", encounters)
    write_csv(OUTPUT_DIR / "raw_diagnosis.csv", diagnoses)

    print(
        "Generated "
        f"{len(patients)} patients, "
        f"{len(facilities)} facilities, "
        f"{len(encounters)} encounters, and "
        f"{len(diagnoses)} diagnosis events."
    )


if __name__ == "__main__":
    main()

