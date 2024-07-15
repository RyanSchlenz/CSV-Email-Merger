import pandas as pd
import json

# Function to standardize email addresses
def standardize_email(email):
    return email.lower().strip() if isinstance(email, str) else email

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

# Access file paths from the configuration
file1_path = config.get('file1_path')
file2_path = config.get('file2_path')
updated_path = config.get('updated_path')

if not file1_path or not file2_path or not updated_path:
    print("Error: One or more file paths are missing in config.json.")
    exit(1)

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

try:
    # Filter out rows where 'name' starts with 'Caller', '+1', or any number
    df1 = df1[~df1['name'].str.match(r'^(Caller|\+1|\d)', na=False)]

    # Standardize email addresses
    df1['email'] = df1['email'].apply(standardize_email)
    df2['UserPrincipalName'] = df2['UserPrincipalName'].apply(standardize_email)  # Assuming 'UserPrincipalName' is the correct column

    # Merge df1 and df2 where both 'email' and 'UserPrincipalName' match
    merged_df = df1.merge(df2[['UserPrincipalName', 'Company', 'EmployeeID']], how='inner', left_on='email', right_on='UserPrincipalName')
    print("\nMerged DataFrame:")
    print(merged_df)

    # Update 'organization' with 'Company' data where it matches
    merged_df['organization'] = merged_df.apply(lambda x: x['Company'] if pd.notna(x['Company']) else x['organization'], axis=1)

    # Route EmployeeID to external_id
    merged_df['external_id'] = merged_df['EmployeeID'].fillna('')  # Replace NaNs with empty string if needed

    print("\nMerged DataFrame after updating organization and routing EmployeeID to external_id:")
    print(merged_df)

    # Select desired columns for the new file
    selected_columns = ['id', 'url', 'name', 'email', 'created_at', 'updated_at', 'time_zone', 'iana_time_zone',
                        'phone', 'shared_phone_number', 'photo', 'locale_id', 'locale', 'role', 'verified',
                        'external_id', 'tags', 'alias', 'active', 'shared', 'shared_agent', 'last_login_at',
                        'two_factor_auth_enabled', 'signature', 'details', 'notes', 'role_type', 'custom_role_id',
                        'moderator', 'ticket_restriction', 'only_private_comments', 'restricted_agent', 'suspended',
                        'default_group_id', 'report_csv', 'user_fields', 'abilities', 'organization']

    # Check if all selected columns are present in the merged DataFrame
    missing_columns = [col for col in selected_columns if col not in merged_df.columns]
    if missing_columns:
        print(f"Error: The following columns are missing in the merged DataFrame: {missing_columns}")
        exit(1)

    # Remove duplicates based on 'id' column
    merged_df.drop_duplicates(subset=['id'], keep='last', inplace=True)

    # Save updated data to the new file
    merged_df[selected_columns].to_csv(updated_path, index=False)
    print(f"\nUpdated data saved successfully to {updated_path}.")
    print("\nFinal DataFrame saved:")
    print(merged_df[selected_columns])

except Exception as e:
    print(f"Error during processing: {e}")
    exit(1)
