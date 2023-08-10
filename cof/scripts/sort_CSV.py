import csv
import re

# Function to extract numeric part from filename


def extract_number(filename):
    match = re.match(r'^(\d+)', filename)
    if match:
        return int(match.group())
    # Return a large value to ensure it comes last in sorting
    return float('inf')


# Read the CSV file
with open('image_links.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # Read and store the header row
    rows = list(reader)    # Read and store the remaining rows

# Sort the rows based on the numeric part of the file names
sorted_rows = sorted(rows, key=lambda row: extract_number(row[0]))

# Write the sorted data back to the CSV file
with open('sorted_image_links.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)  # Write the header row

    for row in sorted_rows:
        writer.writerow(row)

print("CSV file sorted and saved successfully.")
