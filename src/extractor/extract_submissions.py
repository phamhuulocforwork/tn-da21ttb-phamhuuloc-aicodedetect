import pandas as pd
import os
import csv

def extract_submissions():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Input file
    dataset_file = os.path.join(current_dir, '..', 'dataset', 'c', 'csv', 'submission_with_problem.csv')
    base_output_dir = os.path.join(current_dir, '..', 'dataset', 'c', 'human')
    
    print(f"Reading dataset from: {dataset_file}")
    print(f"Output will be organized in: {base_output_dir}")
    
    try:
        # Đọc file CSV
        data = []
        with open(dataset_file, 'r', encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        
        print(f"Loaded {len(data)} submission records")
        
        os.makedirs(base_output_dir, exist_ok=True)
        
        problem_counts = {}
        filtered_count = 0
        
        for row in data:
            submission_id = row['submission_id']
            problem_id = row['problem_id']
            source_code = row['source']
            language_id = row['language_id']
            
            # Lấy submission có language_id là 4 (C++) hoặc 5 (C)
            if language_id not in ['4', '5']:
                filtered_count += 1
                continue
            
            extension = '.cpp' if language_id == '4' else '.c'
            
            problem_dir = os.path.join(base_output_dir, f'problem_{problem_id}')
            os.makedirs(problem_dir, exist_ok=True)
            
            output_file = os.path.join(problem_dir, f'submission_{submission_id}{extension}')
            
            with open(output_file, 'w', encoding='utf-8', newline='') as f:
                f.write(source_code)
            
            problem_counts[problem_id] = problem_counts.get(problem_id, 0) + 1
            
        # In thống kê
        print("\nExport summary:")
        for problem_id, count in sorted(problem_counts.items()):
            print(f"Problem {problem_id}: {count} submissions extracted")
        
        print(f"\nTotal: {sum(problem_counts.values())} files exported successfully")
        print(f"Filtered out: {filtered_count} submissions (not C/C++)")
        
    except FileNotFoundError:
        print(f"Error: Could not find dataset file at {dataset_file}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    extract_submissions() 