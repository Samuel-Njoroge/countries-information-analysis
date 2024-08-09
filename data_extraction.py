import requests
import pandas as pd
import psycopg2
import csv

# Define the URL
url = 'https://restcountries.com/v3.1/all'

# Fetch the data from the URL
response = requests.get(url)
data = response.json()

# Extract required fields
countries_data = []
for country in data:
    # Handle missing data with default values
    country_info = {
        'Country_name': country.get('name', {}).get('common', ''),
        'Independence': country.get('independent', ''),
        'United_Nation_members': country.get('unMember', ''),
        'startOfWeek': country.get('startOfWeek', ''),  
        'Official_country_name': country.get('name', {}).get('official', ''),
        'Common_native_name': country.get('name', {}).get('nativeName', {}).get('eng', {}).get('common', ''),
        'Currency_Code': list(country.get('currencies', {}).keys())[0] if country.get('currencies') else '',
        'Currency_name': list(country.get('currencies', {}).values())[0].get('name', '') if country.get('currencies') else '',
        'Currency_symbol': list(country.get('currencies', {}).values())[0].get('symbol', '') if country.get('currencies') else '',
        'Country_code': country.get('idd', {}).get('root', '') + ''.join(country.get('idd', {}).get('suffixes', [])),
        'Capital': ', '.join(country.get('capital', [])),
        'Region': country.get('region', ''),
        'Sub_region': country.get('subregion', ''),
        'Languages': ', '.join(country.get('languages', {}).values()),
        'Area': country.get('area', ''),
        'Population': country.get('population', ''),
        'Continents': ', '.join(country.get('continents', []))
    }
    countries_data.append(country_info)

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(countries_data)

# Save the DataFrame to a CSV file
df.to_csv('countries_data.csv', index=False)

print("Data has been saved to 'countries_data.csv'.")

# Define the large value and the new country code
large_value = '+120120220320520620720820'
new_country_code = '+1'

# Update the 'Country_code' column where the value matches the large value
df.loc[df['Country_code'] == large_value, 'Country_code'] = new_country_code

# Save the updated DataFrame back to a CSV file
df.to_csv(index=False)

print('Row updated successfully in the CSV file')

# Postgres connection
def get_db_connection():
    connection = psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password='postgres'
    )
    return connection

conn = get_db_connection()

# Creating database table
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    create_table_query = '''CREATE SCHEMA IF NOT EXISTS world;
                            DROP TABLE IF EXISTS world.countries_info;

                            CREATE TABLE world.countries_info(
                            Country_name VARCHAR(150),
                            Independence BOOL,
                            United_Nation_members BOOL,
                            startOfWeek VARCHAR(50),
                            Official_country_name VARCHAR(150),
                            Common_native_name VARCHAR(50),
                            Currency_Code VARCHAR(50),
                            Currency_name VARCHAR(50),
                            Currency_symbol VARCHAR(50),
                            Country_code VARCHAR(50),    
                            Capital VARCHAR(50),    
                            Region VARCHAR(50),
                            Sub_region VARCHAR(50),
                            Languages VARCHAR(150),          
                            Area  VARCHAR(50),        
                            Population INT,
                            Continents VARCHAR(50)
                            );'''
    
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()

create_table()

# Load csv data to database
def load_data_from_csv_to_table(csv_path, table_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            try:
                placeholder = ','.join(['%s'] * len(row))
                query = f'INSERT INTO {table_name} VALUES ({placeholder});'
                cursor.execute(query, row)
            except psycopg2.DataError as e:
                print(f"Error inserting row: {row}")
                print(e)
    conn.commit()
    cursor.close()
    conn.close()


# Load  data to database
countries_csv_path = r'countries_data.csv'
load_data_from_csv_to_table(countries_csv_path, 'world.countries_info')

print('Data Loaded success fully')
