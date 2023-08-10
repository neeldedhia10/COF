import pandas as pd

# Load the CSV file into a DataFrame
csv_file = 'sorted_image_links.csv'  # Replace with the path to your CSV file
df = pd.read_csv(csv_file)

# Modify the "Sharing Link" column
df['Sharing Link'] = "https://drive.google.com/uc?export=view&id=" + df['Sharing Link']

# Write the updated DataFrame back to the CSV file
df.to_csv(csv_file, index=False)

print("Sharing links updated successfully.")
