import pandas as pd
import os
import re

def clean_escape_characters(text):
    if pd.isna(text) or not isinstance(text, str):
        return text

    text = text.replace('\\n', '\n')
    text = text.replace('\\t', ' ')
    text = text.replace('\\r', '')
    text = text.replace('\\ \\ \\ \\ ', ' ')
    text = text.replace('\\ \\ ', ' ')
    text = text.replace('\\ ', ' ')
    text = text.replace('\\\\', '\\')
    text = text.replace('\\"""', '"')    
    text = text.replace('\\"', '"')      
    text = text.replace("\\'", "'")      
    text = re.sub(r'\\u[0-9a-fA-F]{4}', '', text)
    text = re.sub(r'\\x[0-9a-fA-F]{2}', '', text)
    text = re.sub(r'\\[a-zA-Z]', '', text)
    text = re.sub(r'\\+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    text = re.sub(r'""""+', '"', text)
    
    return text

def extract_problem_info():
    input_file = "dataset/metadata/problems.csv"
    output_file = "dataset/metadata/problems_extracted.csv"
    
    try:
        df = pd.read_csv(input_file)
        
        required_columns = ['id', 'name', 'description']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"Missing columns in file: {missing_columns}")
            return False
        
        extracted_df = df[required_columns].copy()
        
        text_columns = ['name', 'description']
        for col in text_columns:
            if col in extracted_df.columns:
                extracted_df[col] = extracted_df[col].apply(clean_escape_characters)
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        extracted_df.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"Extracted {len(extracted_df)} problems to {output_file}.")
        return True
        
    except FileNotFoundError:
        print(f"File not found: {input_file}")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def preview_extracted_data(num_rows=5):
    output_file = "dataset/metadata/problems_extracted.csv"
    
    try:
        df = pd.read_csv(output_file)
        print(f"\nPreview first {num_rows} rows:")
        print("=" * 80)
        for i, row in df.head(num_rows).iterrows():
            print(f"ID: {row['id']}")
            print(f"Name: {row['name']}")
            print(f"Description: {row['description'][:100]}..." if len(str(row['description'])) > 100 else f"Description: {row['description']}")
            print("-" * 40)
            
    except FileNotFoundError:
        print("Extracted file not found. Please run extract_problem_info() first.")
    except Exception as e:
        print(f"Preview error: {str(e)}")

if __name__ == "__main__":
    print("Starting problem data extraction...")
    success = extract_problem_info()
    print("Done!")
