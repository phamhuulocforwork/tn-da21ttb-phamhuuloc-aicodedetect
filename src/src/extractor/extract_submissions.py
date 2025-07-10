import pandas as pd
import os
import csv
import re

def extract_submissions():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    dataset_file = os.path.join(current_dir, '..', 'dataset', 'c', 'csv', 'submission_with_problem.csv')
    base_output_dir = os.path.join(current_dir, '..', 'dataset', 'c', 'human')
        
    try:
        data = []
        with open(dataset_file, 'r', encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        
        print(f"Loaded {len(data)} submission records")
        
        os.makedirs(base_output_dir, exist_ok=True)
        
        problem_counts = {}
        filtered_count = 0
        processed_count = 0
        
        for row in data:
            try:
                submission_id = row['submission_id']
                problem_id = row['problem_id']
                source_code = row['source']
                language_id = row['language_id']
                
                if language_id not in ['4', '5']:
                    filtered_count += 1
                    continue
                
                source_code = process_source_code(source_code)
                
                extension = '.cpp' if language_id == '4' else '.c'
                
                problem_dir = os.path.join(base_output_dir, f'problem_{problem_id}')
                os.makedirs(problem_dir, exist_ok=True)
                
                output_file = os.path.join(problem_dir, f'submission_{submission_id}{extension}')
                
                with open(output_file, 'w', encoding='utf-8', newline='') as f:
                    f.write(source_code)
                
                problem_counts[problem_id] = problem_counts.get(problem_id, 0) + 1
                processed_count += 1
                
                if processed_count % 100 == 0:
                    print(f"Progress: {processed_count} submissions processed")
                
            except Exception as e:
                print(f"Error processing submission {row.get('submission_id', 'unknown')}: {str(e)}")
                continue
            
        print("\nExport summary:")
        for problem_id, count in sorted(problem_counts.items(), key=lambda x: int(x[0])):
            print(f"Problem {problem_id}: {count} submissions extracted")
        
        print(f"\nTotal: {sum(problem_counts.values())} files exported successfully")
        print(f"Filtered out: {filtered_count} submissions (not C/C++)")
        
    except FileNotFoundError:
        print(f"Error: Could not find dataset file at {dataset_file}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

def process_source_code(source_code):
    """
    Xử lý source code để khôi phục các ký tự đặc biệt từ định dạng escape trong CSV
    """
    if source_code is None:
        return ""
    
    original_code = source_code
    
    processed_code = re.sub(r'""([^"]*?)""', r'"\1"', source_code)
    
    processed_code = re.sub(r'\\+"', '"', processed_code)
    
    processed_code = processed_code.replace('\\\\', '\\')
    
    escape_chars = {
        '\\n': '\n',
        '\\t': '\t',
        '\\r': '\r',
        '\\"': '"'
    }
    
    for escaped, unescaped in escape_chars.items():
        processed_code = processed_code.replace(escaped, unescaped)
    
    processed_code = re.sub(r'\\+(%[diouxXfFeEgGaAcspn])', r'\1', processed_code)
    
    processed_code = processed_code.replace('\\\"', '"')
    
    processed_code = re.sub(r'""+', '"', processed_code)
    processed_code = re.sub(r'""([^"])', r'"\1', processed_code)
    processed_code = re.sub(r'([^"])+""', r'\1"', processed_code)
    
    if '""' in processed_code:
        processed_code = processed_code.replace('""', '"')
    
    suspicious_patterns = ['\\\"', '\\\\', '""']
    for pattern in suspicious_patterns:
        if pattern in processed_code:
            print(f"Warning: Still found '{pattern}' after processing in submission")
            print(f"  Original: {original_code[:100]}...")
            print(f"  Processed: {processed_code[:100]}...")
    
    return processed_code

if __name__ == "__main__":
    extract_submissions() 