import csv
from main.models import Lawyer, LawCategory

with open("lawyers_dataset.csv", newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:
        category_name = row['specialization'].strip()

        # create category if it doesn't exist
        category, created = LawCategory.objects.get_or_create(name=category_name)

        Lawyer.objects.create(
            name=row['name'],
            specialization=category,
            experience=int(row['experience']),
            email=row['email'],
            phone=row['phone'],
            location=row['location']
        )

print("Lawyers imported successfully!")