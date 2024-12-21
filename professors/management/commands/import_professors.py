# comments/management/commands/import_professors.py

import pandas as pd
from django.core.management.base import BaseCommand
from professors.models import Professor


class Command(BaseCommand):
    help = 'Imports professors from an Excel file to the database'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str,
                            help='Path to the Excel file containing professors')

    def handle(self, *args, **kwargs):
        excel_file = kwargs['excel_file']
        added_count = 0  # To track how many professors are added

        try:
            # Read the Excel file into a pandas DataFrame
            df = pd.read_excel(excel_file)

            # Loop through each row in the DataFrame and create Professor objects
            for index, row in df.iterrows():
                professor_name_fa = row['نام استاد']
                department_fa = row['دانشکده درس']
                
                professor_name_en = row['en_name']
                department_en = row['en_fac']
                try:
                # Create and save the professor if it's not already in the database
                    if not Professor.objects.filter(name_fa=professor_name_fa,
                                                name_en=professor_name_en).exists():
                    
                        Professor.objects.create(name_fa=professor_name_fa, 
                                                department_fa=department_fa,
                                                name_en=professor_name_en, department_en=department_en)
                        added_count += 1  # Increment the counter
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error: {str(e)} {professor_name_fa} {department_fa} {professor_name_en} {department_en}"))
                    continue
            # Output the result
            self.stdout.write(self.style.SUCCESS(
                f"Successfully added {added_count} professors"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
