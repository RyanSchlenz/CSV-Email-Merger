# CSV-Email-Merger
Script Overview
The script is designed to process two CSV files (file1 and file2), standardize email addresses, merge data based on matching emails/UserPrincipalName, and output a standardized CSV file.

**Dependencies**
pandas: Used for data manipulation and handling CSV files.
json: Used for reading the configuration stored in a JSON file.

**Functions**
standardize_email(email):
Purpose: Standardizes email addresses by converting them to lowercase and stripping whitespace.
Parameters: email (string)
Returns: Standardized email address or original input if not a string.
Error Handling
Handles errors such as missing files (FileNotFoundError), empty data in CSV (pd.errors.EmptyDataError), JSON decoding issues (json.JSONDecodeError), and general exceptions (Exception).

**Steps**
**Load Configuration**

Loads configuration settings from config.json which includes file paths (file1_path, file2_path, updated_path).
Read CSV Files

Reads file1 and file2 into pandas DataFrames (df1, df2).
Skips metadata rows in file2 using skiprows and sets index_col to False.
Data Processing

Filters df1 to exclude rows where the 'name' column starts with specific patterns (Caller, +1, or any digit).
Standardizes email addresses in both DataFrames using standardize_email().
Data Merging

Merges df1 and df2 based on matching email addresses (email and UserPrincipalName).
Updates 'organization' with 'Company' data where available.
Routes 'EmployeeID' to 'external_id'.
Column Selection

Defines selected_columns which lists all desired columns for the final output.
Checks if all selected columns exist in the merged DataFrame.
Data Output

Removes duplicates based on 'id' column.
Saves the selected columns of the merged DataFrame to updated_path as a CSV file.
Example Usage
  
 
**script.py**
Example Output
Displays intermediate DataFrames (df1, df2, merged_df) during execution.
Prints messages indicating successful execution or errors encountered.

**Documentation Tips**
Include inline comments explaining complex logic or operations.
Document function purpose, parameters, and return values.
Add error handling explanations and expected exceptions.
Provide examples of typical usage scenarios.
