import pandas as pd
import flag  # To convert country ISO codes to flag emojis

# Load the dataset (assuming it already contains ISO codes)
file_path = '/mnt/data/transformed_migrant_data_with_flags.csv'  # Adjust path if necessary
df = pd.read_csv(file_path)

# Function to convert ISO code to flag emoji
def get_country_flag(iso_code):
    try:
        return flag.flag(iso_code)  # Convert ISO code to flag
    except KeyError:
        return "🏳️"  # Default white flag for ISO codes not found

# Assuming there is a column for ISO country codes (adjust column name if necessary)
df['Country_Flag'] = df['iso_country_code'].apply(get_country_flag)

# Create a new combined field with country name and flag
df['Country_Name_Flag'] = df['country_name'] + ' ' + df['Country_Flag']

# Save the updated dataset
df.to_csv('/mnt/data/transformed_migrant_data_with_flags.csv', index=False)
print(df[['country_name', 'iso_country_code', 'Country_Flag', 'Country_Name_Flag']].head())
