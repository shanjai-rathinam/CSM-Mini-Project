import pandas as pd
import json
import os

def transform_legacy_data():
    """
    This script simulates the ETL Transform step for migrating legacy
    IT incident data to a modern, cloud-native format.
    """
    # Define file paths
    # Assumes the script is run from the root directory of the project
    input_csv_path = os.path.join('data', 'legacy_incidents_data.csv')
    output_json_path = os.path.join('data', 'cloud_ready_incidents.json')

    print(f"Reading legacy data from {input_csv_path}...")

    # 1. EXTRACT: Read the legacy CSV data
    try:
        # Use a robust parser, handle potential bad lines
        df = pd.read_csv(input_csv_path, on_bad_lines='skip')
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_csv_path}")
        print("Please ensure you have downloaded the data from Kaggle and placed it correctly.")
        return

    # 2. TRANSFORM: Clean and restructure the data
    print("Transforming data for the cloud...")

    # Rename columns for clarity and consistency
    df.rename(columns={
        'number': 'incident_id',
        'short_description': 'summary',
        'caller_id': 'caller',
        'priority': 'priority_level'
    }, inplace=True)

    # Select only the columns needed for the new system
    # This reduces data size and simplifies the new application
    df_transformed = df[['incident_id', 'summary', 'caller', 'priority_level', 'sys_created_on']].copy()

    # Data Cleaning and Formatting
    # Convert dates to ISO 8601 format, which is a cloud standard
    df_transformed['creation_timestamp'] = pd.to_datetime(df_transformed['sys_created_on']).dt.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Fill missing values (NaN) with a placeholder
    df_transformed['summary'].fillna('No summary provided', inplace=True)
    df_transformed['caller'].fillna('Unknown', inplace=True)

    # Drop the old timestamp column
    df_transformed.drop(columns=['sys_created_on'], inplace=True)

    # Convert the cleaned DataFrame to a list of dictionaries (JSON-like structure)
    cloud_ready_data = df_transformed.to_dict(orient='records')

    # 3. LOAD (Simulated): Save the transformed data as a JSON file
    print(f"Saving cloud-ready data to {output_json_path}...")
    with open(output_json_path, 'w') as f:
        json.dump(cloud_ready_data, f, indent=4)

    print("\nTransformation complete!")
    print(f"{len(cloud_ready_data)} records processed successfully.")

if __name__ == "__main__":
    # Ensure 'data' directory exists
    if not os.path.exists('data'):
        os.makedirs('data')
    transform_legacy_data()
