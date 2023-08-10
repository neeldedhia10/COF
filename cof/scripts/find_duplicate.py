import csv

# Path to your CSV file
csv_file_path = 'sorted_image_links.csv'

# Read the CSV file and detect duplicate filenames
def find_duplicate_filenames(csv_path):
    filename_count = {}
    duplicate_filenames = []

    with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row

        for row in reader:
            if len(row) >= 1:
                filename = row[0].split('.')[0]
                if filename in filename_count:
                    if filename_count[filename] == 1:
                        duplicate_filenames.append(filename)
                    filename_count[filename] += 1
                else:
                    filename_count[filename] = 1

    return duplicate_filenames

# Find and print duplicate filenames
duplicate_files = find_duplicate_filenames(csv_file_path)
if duplicate_files:
    print("Duplicate filenames found:")
    for filename in duplicate_files:
        print(filename)
else:
    print("No duplicate filenames found.")

