import pandas as pd
import os
import csv
import re

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
        processed_count = 0
        
        for row in data:
            try:
                submission_id = row['submission_id']
                problem_id = row['problem_id']
                source_code = row['source']
                language_id = row['language_id']
                
                # Lấy submission có language_id là 4 (C++) hoặc 5 (C)
                if language_id not in ['4', '5']:
                    filtered_count += 1
                    continue
                
                # Xử lý source code để khôi phục các ký tự đặc biệt
                source_code = process_source_code(source_code)
                
                extension = '.cpp' if language_id == '4' else '.c'
                
                problem_dir = os.path.join(base_output_dir, f'problem_{problem_id}')
                os.makedirs(problem_dir, exist_ok=True)
                
                output_file = os.path.join(problem_dir, f'submission_{submission_id}{extension}')
                
                with open(output_file, 'w', encoding='utf-8', newline='') as f:
                    f.write(source_code)
                
                problem_counts[problem_id] = problem_counts.get(problem_id, 0) + 1
                processed_count += 1
                
                # In tiến độ mỗi 100 submissions
                if processed_count % 100 == 0:
                    print(f"Progress: {processed_count} submissions processed")
                
            except Exception as e:
                print(f"Error processing submission {row.get('submission_id', 'unknown')}: {str(e)}")
                continue
            
        # In thống kê
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
    
    # Tạo bản sao để theo dõi thay đổi
    original_code = source_code
    
    # 1. Xử lý trường hợp ký tự escape ""text"" (nháy kép đôi)
    processed_code = re.sub(r'""([^"]*?)""', r'"\1"', source_code)
    
    # 2. Xử lý chuỗi \\" thành "
    processed_code = re.sub(r'\\+"', '"', processed_code)
    
    # 3. Xử lý dấu backslash kép thành dấu backslash đơn
    processed_code = processed_code.replace('\\\\', '\\')
    
    # 4. Đảm bảo các ký tự escape phổ biến được xử lý đúng
    escape_chars = {
        '\\n': '\n',
        '\\t': '\t',
        '\\r': '\r',
        '\\"': '"'
    }
    
    for escaped, unescaped in escape_chars.items():
        processed_code = processed_code.replace(escaped, unescaped)
    
    # 5. Xử lý đặc biệt cho các định dạng trong printf/scanf
    processed_code = re.sub(r'\\+(%[diouxXfFeEgGaAcspn])', r'\1', processed_code)
    
    # 6. Xử lý các trường hợp bất thường
    processed_code = processed_code.replace('\\\"', '"')
    
    # 7. Xử lý dấu nháy kép lặp lại (mẫu "")
    processed_code = re.sub(r'""+', '"', processed_code)
    processed_code = re.sub(r'""([^"])', r'"\1', processed_code)
    processed_code = re.sub(r'([^"])+""', r'\1"', processed_code)
    
    # 8. Kiểm tra lại toàn bộ để đảm bảo tất cả nháy kép đều được xử lý
    if '""' in processed_code:
        processed_code = processed_code.replace('""', '"')
    
    # Debug: In ra báo cáo nếu còn ký tự escape bất thường
    suspicious_patterns = ['\\\"', '\\\\', '""']
    for pattern in suspicious_patterns:
        if pattern in processed_code:
            print(f"Warning: Still found '{pattern}' after processing in submission")
            # Thêm debug info
            print(f"  Original: {original_code[:100]}...")
            print(f"  Processed: {processed_code[:100]}...")
    
    return processed_code

if __name__ == "__main__":
    extract_submissions() 