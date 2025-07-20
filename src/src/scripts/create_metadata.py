import os
import pandas as pd

def create_metadata(dataset_path='dataset/code/c', output_csv='dataset/metadata/metadata.csv'):
    metadata = []
    
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith('.cpp'):
                parts = root.split(os.sep)
                if 'ai' in parts:
                    label = 'ai'
                elif 'human' in parts:
                    label = 'human'
                else:
                    continue
                
                problem_id = parts[-1] if parts[-1].startswith('problem_') else None
                
                submission_id = os.path.splitext(file)[0]
                
                rel_path = os.path.join(root, file)
                
                
                metadata.append({
                    'file_path': rel_path,
                    'problem_id': problem_id,
                    'submission_id': submission_id,
                    'label': label,
                })
    
    df = pd.DataFrame(metadata)
    df.to_csv(output_csv, index=False)
    print(f"Metadata saved to {output_csv}")

if __name__ == '__main__':
    create_metadata() 