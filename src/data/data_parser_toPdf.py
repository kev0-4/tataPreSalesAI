'''
THIS SHIT DOES NOT WORK! FFS SOME ISSUE IN SOME COMMAS IN SOME INDEX IN EXTRACTED_DATA 
CANT SEEM TO FIGURE IT OUT
'''
import re
import json
import pandas as pd

def fix_json_format(data):
    # Fix single quotes to double quotes
    data = data.replace("'", '"')
    
    # Ensure keys and string values are properly quoted
    data = re.sub(r'(?<!")(\w+)(?=:)', r'"\1"', data)
    
    # Fix trailing commas before closing braces and brackets
    data = re.sub(r',(\s*[\]}])', r'\1', data)
    
    # Fix unescaped double quotes inside strings
    data = re.sub(r'\\\\"', r'\\"', data)
    
    return data

def process_entry(entry):
    try:
        # Attempt to decode JSON entry
        entry_data = json.loads(entry)
        return entry_data
    except json.JSONDecodeError as e:
        # Print specific error details
        print(f"Error decoding JSON entry: {e}")
        print(f"Problematic entry: {entry}")
        # Return None to skip this entry
        return None

def convert_to_dataframe(input_filepath):
    with open(input_filepath, 'r') as f:
        raw_data = f.read()
    
    # Attempt to fix the JSON format
    fixed_data = fix_json_format(raw_data)
    
    # Prepare data for DataFrame
    rows = []
    entries = fixed_data.strip().strip('[]').split('}, {')
    
    # Handle edge cases for first and last entry
    entries[0] = '{' + entries[0].lstrip('{')
    entries[-1] = entries[-1].rstrip('}') + '}'
    
    for entry in entries:
        entry_data = process_entry(entry)
        if entry_data:
            for item in entry_data:
                for title, content_list in item.items():
                    for sub_item in content_list:
                        for question, answer in sub_item.items():
                            rows.append({'Title': title, 'Question': question, 'Answer': answer})
    
    df = pd.DataFrame(rows)
    return df

# Usage
input_filepath = 'C:/Users/lemon/Desktop/tata/tatapresalesai/data/raw/extracted_data.txt'
df = convert_to_dataframe(input_filepath)
print(df.head())
