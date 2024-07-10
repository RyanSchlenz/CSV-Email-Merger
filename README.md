# CSV-Email-Merger
Script Documentation: Merging and Updating CSV Files
Overview
This script reads two CSV files, standardizes email addresses, merges the data based on these standardized email addresses, updates specific fields, and saves the updated data to a new CSV file. The script utilizes a configuration file (config.json) to manage file paths and employs error handling to ensure robustness.

**Prerequisites**
Python 3.x
pandas library
json library
Configuration
The script relies on a configuration file named config.json to specify the file paths for the input and output CSV files. The configuration file should be structured as follows:

json
{
  "file1_path": "path/to/first/csv/file.csv",
  "file2_path": "path/to/second/csv/file.csv",
  "updated_path": "path/to/output/csv/file.csv"
}
Script Description
Imports and Function Definition
python
import pandas as pd
import json

# Function to standardize email addresses
def standardize_email(email):
   return email.lower().strip() if isinstance(email, str) else email
Imports: Imports the necessary libraries.
Function: Defines a function to standardize email addresses by converting them to lowercase and stripping any leading/trailing whitespace.
Load Configuration
python
try:
    # Load the configuration file
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    print("Error: config.json file not found.")
    exit(1)
except json.JSONDecodeError:
    print("Error: Failed to decode JSON from config.json.")
    exit(1)
Loading Configuration: Reads the configuration file and handles potential errors such as file not found or JSON decoding errors.
Access and Validate File Paths
python
file1_path = config.get('file1_path')
file2_path = config.get('file2_path')
updated_path = config.get('updated_path')

if not file1_path or not file2_path or not updated_path:
    print("Error: One or more file paths are missing in config.json.")
    exit(1)
File Path Extraction: Extracts file paths from the configuration and checks for their presence.
Read CSV Files
python
try:
    # Read CSV files
    df1 = pd.read_csv(file1_path)
    df2 = pd.read_csv(file2_path, skiprows=1, index_col=False)  # Skip the first row (metadata)
except FileNotFoundError as e:
    print(f"Error: {e.filename} not found.")
    exit(1)
except pd.errors.EmptyDataError:
    print("Error: No data in one of the CSV files.")
    exit(1)

print("DataFrame 1 (file1):")
print(df1)
print("\nDataFrame 2 (file2):")
print(df2)
Reading CSV Files: Reads the CSV files into DataFrames and handles errors such as file not found or empty data files.
Debugging Output: Prints the contents of the DataFrames for verification.
Data Processing
python
try:
    # Standardize email addresses
    df1['email'] = df1['email'].apply(standardize_email)
    df2['UserPrincipalName'] = df2['UserPrincipalName'].apply(standardize_email)  # Assuming 'UserPrincipalName' is the correct column

    # Merge df1 and df2 on standardized 'email' (left join)
    merged_df = df1.merge(df2[['UserPrincipalName', 'Company', 'EmployeeID']], how='left', left_on='email', right_on='UserPrincipalName')
    print("\nMerged DataFrame:")
    print(merged_df)

    # Update 'organization' with 'Company' data where it matches
    merged_df['organization'] = merged_df.apply(lambda x: x['Company'] if pd.notna(x['Company']) else x['organization'], axis=1)

    # Add EmployeeID to File 1 where available
    merged_df['EmployeeID'] = merged_df['EmployeeID'].fillna('')  # Replace NaNs with empty string if needed
    print("\nMerged DataFrame after updating organization and adding EmployeeID:")
    print(merged_df)
Standardize Emails: Applies the standardize_email function to standardize email addresses in both DataFrames.
Merge DataFrames: Merges df1 and df2 on the standardized email address, using a left join.
Update Fields: Updates the 'organization' field with 'Company' data where it matches, and fills the 'EmployeeID' field with available data.
Debugging Output: Prints the merged DataFrame before and after updates for verification.
Validate Columns and Save Updated Data
python

    # Select desired columns for the new file
    selected_columns = ['id', 'url', 'name', 'email', 'created_at', 'updated_at', 'time_zone', 'iana_time_zone',
                        'phone', 'shared_phone_number', 'photo', 'locale_id', 'locale', 'role', 'verified',
                        'external_id', 'tags', 'alias', 'active', 'shared', 'shared_agent', 'last_login_at',
                        'two_factor_auth_enabled', 'signature', 'details', 'notes', 'role_type', 'custom_role_id',
                        'moderator', 'ticket_restriction', 'only_private_comments', 'restricted_agent', 'suspended',
                        'default_group_id', 'report_csv', 'user_fields', 'abilities', 'organization', 'EmployeeID']

    # Check if all selected columns are present in the merged DataFrame
    missing_columns = [col for col in selected_columns if col not in merged_df.columns]
    if missing_columns:
        print(f"Error: The following columns are missing in the merged DataFrame: {missing_columns}")
        exit(1)

    # Save updated data to the new file
    merged_df[selected_columns].to_csv(updated_path, index=False)
    print(f"\nUpdated data saved successfully to {updated_path}.")
    print("\nFinal DataFrame saved:")
    print(merged_df[selected_columns])

except Exception as e:
    print(f"Error during processing: {e}")
    exit(1)
Column Selection: Defines the columns to be included in the new CSV file.
Column Validation: Checks if all selected columns exist in the merged DataFrame.
Save Data: Saves the updated DataFrame to the specified output path.
General Error Handling: Catches and prints any exceptions that occur during processing.
Execution
Run the script using a Python interpreter:

**bash**
python script_name.py
Ensure that the config.json file is in the same directory as the script or provide the correct path.

**Debugging**
The script includes several print statements to output the DataFrames at various stages for debugging purposes. If the script fails, the error messages will provide guidance on what went wrong.
