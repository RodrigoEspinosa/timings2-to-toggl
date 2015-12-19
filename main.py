import csv
import argparse
from datetime import datetime

MATCH_ONE_TO_ONE = ('Client', 'Project',)
TARGET_FIELDNAMES = ('Email', 'Client', 'Project', 'Task', 'Description',
                     'Billable', 'Start date', 'Start time', 'Duration',
                     'Tags',)

SOURCE_DATE_FORMAT = '%m/%d/%y, %I:%M %p'

# Parse the program arguments.
parser = argparse.ArgumentParser(description='Convert Timings2 csv format '
                                             'to Toggl format.')
parser.add_argument('file', help='the original csv file path')
parser.add_argument('email', help='user email for the target file')
args = parser.parse_args()

# Get the path for the target file.
target_filename = '{path}_converted.{extension}'.format(**{
    'path': args.file.rsplit('.')[0],
    'extension': args.file.rsplit('.')[1]
})

# Open the source and target file.
source_file = open(args.file, 'r')
target_file = open(target_filename, 'w')

# Parse and save the source csv file into the target csv file.
reader = csv.DictReader(source_file)
writer = csv.DictWriter(target_file, fieldnames=TARGET_FIELDNAMES)

# Write the headers.
writer.writeheader()

# Iterate over all the entries in the source file.
for source_entry in reader:

    # Initialize the dictonary by picking from the existing entry.
    target_entry = {key: source_entry[key] for key in MATCH_ONE_TO_ONE}

    # Rename columns.
    target_entry['Tags'] = source_entry['Subproject'].lower()
    target_entry['Description'] = source_entry['Notes']

    # Convert the date format.
    source_date = datetime.strptime(source_entry['Start'], SOURCE_DATE_FORMAT)
    target_entry['Start date'] = source_date.strftime('%Y-%m-%d')
    target_entry['Start time'] = source_date.strftime('%H:%M:%S')

    # Add seconds to the duration (since Timings2 do not track them).
    target_entry['Duration'] = source_entry['Duration'] + ':00'

    # Add the email to the target entry.
    target_entry['Email'] = args.email

    # Write the entry into the target csv file.
    writer.writerow(target_entry)

# Close both files.
source_file.close()
target_file.close()
