# Required libraries
import pandas as pd
import country_converter as coco
from pycountry_convert import country_alpha3_to_country_alpha2, country_alpha2_to_continent_code, convert_continent_code_to_continent_name

# Load the dataset
file_path = 'data/arrivals_soe.csv'  # Replace with your file path
data = pd.read_csv(file_path)

# Convert ISO3 country codes to country names
data['country_name'] = coco.convert(names=data['country'], to='name_short')

# Extract year from the 'date' column
data['year'] = pd.to_datetime(data['date']).dt.year

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

# Aggregating data by country and year
grouped_data = data.groupby(['country_name', 'year']).agg(
    Male_Migrants=('arrivals_male', 'sum'),
    Female_Migrants=('arrivals_female', 'sum'),
    Total_Migrants=('arrivals', 'sum')
).reset_index()

# Add continent back for filtering
grouped_data = grouped_data.merge(data[['country_name', 'continent']].drop_duplicates(), on='country_name', how='left')

# Save the transformed data to a new file
grouped_data.to_csv('transformed_migrant_data.csv', index=False)

# Example: Filtering by year and continent
# Filter for Asia in 2023
asia_2023_data = grouped_data[(grouped_data['continent'] == 'Asia') & (grouped_data['year'] == 2023)]
print(asia_2023_data)
