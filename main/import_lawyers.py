import csv
from main.models import Lawyer, LawCategory

CATEGORY_MAP = {
    "criminal": "Criminal Law",
    "civil": "Civil Law",
    "family": "Family Law",
    "corporate": "Corporate Law",
    "cyber": "Cyber Law",
    "property": "Property Law",
    "labor": "Labor Law",
    "environment": "Environmental Law",
    "intellectual": "Intellectual Property Law",
    "employee": "Employee Law",
    "consumer": "Consumer Law"
}

with open("lawyers.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        spec = row["specialization"].lower()

        category_name = None
        for key in CATEGORY_MAP:
            if key in spec:
                category_name = CATEGORY_MAP[key]
                break

        if not category_name:
            print("❌ No category for:", row["name"])
            continue

        # ✅ FIXED HERE
        category, _ = LawCategory.objects.get_or_create(
            name=category_name.strip().title()
        )

        Lawyer.objects.create(
            name=row["name"],
            email=row["email"],
            phone=row["phone"],
            specialization=row["specialization"],
            experience=int(row["experience"]),
            location=row["location"],
            category=category
        )

print("✅ Lawyers Imported Successfully")