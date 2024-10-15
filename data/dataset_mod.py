import pandas as pd
import jenkspy

# Load your dataset
file_path = 'data/world_map_arrival_data.csv'  # Replace with your actual file path
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"File not found: {file_path}")
    exit()

# Calculate natural breaks for each year (2020 to 2024)
years = ['2020', '2021', '2022', '2023', '2024']
breaks_dict = {}

for year in years:
    # Remove missing or zero values and drop NaNs
    data = df[year].dropna()
    data = data[data > 0]  # Exclude zero or negative values if needed
    
    if data.empty:
        print(f"No valid data for year {year}")
        continue
    
    breaks = jenkspy.jenks_breaks(data, n_classes=5)  # Use n_classes instead of nb_class
    breaks_dict[year] = breaks

# Print the calculated breaks for each year
for year, breaks in breaks_dict.items():
    print(f"Natural breaks for {year}: {breaks}")
