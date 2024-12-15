# comments/management/commands/import_professors.py

import pandas as pd
from django.core.management.base import BaseCommand
from professors.models import Professor

class Command(BaseCommand):
    help = 'Imports professors from an Excel file to the database'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to the Excel file containing professors')

    def handle(self, *args, **kwargs):
        excel_file = kwargs['excel_file']
        added_count = 0  # To track how many professors are added

        try:
            # Read the Excel file into a pandas DataFrame
            df = pd.read_excel(excel_file)

            # Loop through each row in the DataFrame and create Professor objects
            for index, row in df.iterrows():
                professor_name = row['نام استاد']
                department = row['دانشکده درس']

                # Create and save the professor if it's not already in the database
                if not Professor.objects.filter(name=professor_name, department=department).exists():
                    Professor.objects.create(name=professor_name, department=department)
                    added_count += 1  # Increment the counter

            # Output the result
            self.stdout.write(self.style.SUCCESS(f"Successfully added {added_count} professors"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
