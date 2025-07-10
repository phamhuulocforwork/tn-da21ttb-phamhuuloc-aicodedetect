import pandas as pd
import os
import csv

def join_datasets():
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_dir = os.path.join(current_dir, 'dataset', 'c', 'csv')
    
    # Input files
    submission_file = os.path.join(csv_dir, 'submission.csv')
    source_file = os.path.join(csv_dir, 'submission_source.csv')
    
    # Output file
    output_file = os.path.join(csv_dir, 'submission_with_problem.csv')
    
    print(f"Reading submission data from: {submission_file}")
    print(f"Reading source code data from: {source_file}")
    print(f"Output will be written to: {output_file}")
    
    try:
        submissions_df = pd.read_csv(submission_file, encoding='utf-8')
        
        source_data = []
        with open(source_file, 'r', encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                source_data.append(row)
        
        source_df = pd.DataFrame(source_data)
        
        print(f"Loaded {len(submissions_df)} submission records")
        print(f"Loaded {len(source_df)} source code records")
        
        print("Submission data columns:", submissions_df.columns.tolist())
        print("Source data columns:", source_df.columns.tolist())
        
        source_df['submission_id'] = source_df['submission_id'].astype(int)
        submissions_df['id'] = submissions_df['id'].astype(int)
        
        merged_df = pd.merge(
            source_df,
            submissions_df[['id', 'problem_id', 'language_id']],
            left_on='submission_id',
            right_on='id',
            suffixes=('', '_submission')
        )
        
        result_df = merged_df[['id', 'source', 'submission_id', 'problem_id', 'language_id']]
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            
            writer.writerow(['id', 'source', 'submission_id', 'problem_id', 'language_id'])
            
            for _, row in result_df.iterrows():
                writer.writerow([
                    row['id'],
                    row['source'],
                    row['submission_id'],
                    row['problem_id'],
                    row['language_id']
                ])
        
        print(f"Successfully combined datasets into {output_file}")
        print(f"Total records in combined dataset: {len(result_df)}")
        
    except FileNotFoundError as e:
        print(f"Error: Could not find input file: {str(e)}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    join_datasets() 