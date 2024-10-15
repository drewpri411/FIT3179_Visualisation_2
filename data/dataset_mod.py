# Required libraries
import pandas as pd
import country_converter as coco
from pycountry_convert import country_alpha3_to_country_alpha2, country_alpha2_to_continent_code, convert_continent_code_to_continent_name

# Load the dataset
file_path = 'data/arrivals.csv'  # Replace with your local file path
data = pd.read_csv(file_path)

# Convert ISO3 country codes to country names
data['country_name'] = coco.convert(names=data['country'], to='name_short')

# Extract year and month as text from the 'date' column
data['year'] = pd.to_datetime(data['date']).dt.year
data['month'] = pd.to_datetime(data['date']).dt.strftime('%B')

# Function to map country ISO3 to continent
def get_continent_from_iso3(iso3_code):
    try:
        alpha2_code = country_alpha3_to_country_alpha2(iso3_code)
        continent_code = country_alpha2_to_continent_code(alpha2_code)
        return convert_continent_code_to_continent_name(continent_code)
    except KeyError:
        return None

# Add continent information
data['continent'] = data['country'].apply(get_continent_from_iso3)

# Drop rows where continent is not identified (e.g., ALL entries)
data_filtered = data.dropna(subset=['continent'])

# Group the data by country, continent, year, and month, and calculate the monthly total
grouped_data = data_filtered.groupby(['country_name', 'continent', 'year', 'month']).agg(
    monthly_total=('arrivals', 'sum')
).reset_index()

# Save the transformed data to a new file
output_file_path = 'transformed_arrivals_data.csv'
grouped_data.to_csv(output_file_path, index=False)

print(f"Transformed data saved to {output_file_path}")
