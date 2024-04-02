import pandas as pd
import fastavro

# Function to read Avro file into memory
def read_avro_file(file_path):
    with open(file_path, 'rb') as avro_file:
        avro_reader = fastavro.reader(avro_file)
        return pd.DataFrame(avro_reader)

# Read data from JSON and CSV files
df_a = pd.read_json('CityListA.json')
df_c = pd.read_csv('CityListC.csv', encoding='utf-8')  # Specify the correct encoding

# Read data from Avro file using the custom function
df_b = read_avro_file('CityListB.avro')

# Combine dataframes into a single dataframe and do not use the index values on the concatenation axis
combined_df = pd.concat([df_a, df_b, df_c], ignore_index=True)

# Automatically detect the 'Name' column
name_column = None
for column in combined_df.columns:
    if 'Name' in column.lower():
        name_column = column
        break

# Check if the required columns are found
required_columns = ['Name', 'CountryCode', 'Population']

if all(col in combined_df.columns for col in required_columns):
    # Set 'Name' as the index using inplace command for the combined file
    combined_df.set_index('Name', inplace=True)

    # Drop duplicates based on the index (which is now 'Name')
    # Explanation: combined_df.index.duplicated(keep='first') will return boolean list where 'True' indicates 
    # that the index is duplicated. 
    # The 'keep=first' parameter means that the first occurrence of a duplicate is marked as False, 
    # and subsequent occurrences are marked as True.
    # By asking for '~combined_df.index.duplicated(keep='first')' it means to get the NOT of the result, 
    # so 'True' is 'False' and via versa.
    # Hence, the below statement, will use boolean indexing to select only the rows where the corresponding 
    # index is not a duplicate. 
    # Rows with duplicate indices are filtered out, and the resulting DataFrame is assigned back to combined_df.
    combined_df = combined_df[~combined_df.index.duplicated(keep='first')]

    # Reset the index to numeric values (modifying the existing index of the df instead of adding 
    # a new column "index" which is the default (without inplace). This is used cause we have dropped duplicates
    # and need to alter the index to the remaining lines
    combined_df.reset_index(inplace=True)

    # Sort the dataframe alphabetically by city name, using ignore_index=True to set the resulting axis to 
    # be labeled as 0,1,... and so forth.
    combined_df = combined_df.sort_values(by='Name', ignore_index=True)

    # Write the combined and sorted dataframe to a CSV file with UTF-8 encoding
    combined_df.to_csv('CombinedCityList.csv', index=False, encoding='utf-8')

    print("Combined and sorted data written to CombinedCityList.csv with UTF-8 encoding")

    # Print total number of rows in the result file, using 'f' before the print statement as I want to execute
    # the expression within the curly braces.
    print(f"Total number of rows in the result file: {len(combined_df)}")

    # Print City name with the most Population in the file
    # Here, the "combined_df['Population'].idxmax()" finds the index (row label) where the maximum value 
    # occurs in the 'Population' columnm, while using "loc" on that will select the row with the index 
    # returned by idxmax() and the column 'Name'.
    city_with_max_population = combined_df.loc[combined_df['Population'].idxmax(), 'Name']
    print(f"City with the most Population: {city_with_max_population}")

    # Print total population of all Cities that have code name == "BRA"
    # Using the same concept as above with sum() function
    total_population_bra = combined_df.loc[combined_df['CountryCode'] == 'BRA', 'Population'].sum()
    print(f"Total population of all Cities with code name 'BRA': {total_population_bra}")
else:
    print("Error: One or more required columns not found in the combined dataframe.")
