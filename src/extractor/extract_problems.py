import pandas as pd
import os

def extract_problem_info():
    input_file = "src/dataset/c/csv/problems.csv"
    
    output_file = "src/dataset/c/csv/problems_extracted.csv"
    
    try:
        df = pd.read_csv(input_file)
        
        required_columns = ['id', 'name', 'description']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"Các cột sau không tồn tại trong file: {missing_columns}")
            return False
        
        extracted_df = df[required_columns].copy()
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        extracted_df.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"Đã extract thành công {len(extracted_df)} bài toán!")
        print(f"File output: {output_file}")
        print(f"Các cột đã extract: {', '.join(required_columns)}")
        
        return True
        
    except FileNotFoundError:
        print(f"Không tìm thấy file {input_file}")
        return False
    except Exception as e:
        print(f"{str(e)}")
        return False

def preview_extracted_data(num_rows=5):
    output_file = "src/dataset/c/csv/problems_extracted.csv"
    
    try:
        df = pd.read_csv(output_file)
        print(f"\n👀 Preview {num_rows} dòng đầu tiên:")
        print("=" * 80)
        for i, row in df.head(num_rows).iterrows():
            print(f"ID: {row['id']}")
            print(f"Name: {row['name']}")
            print(f"Description: {row['description'][:100]}..." if len(str(row['description'])) > 100 else f"Description: {row['description']}")
            print("-" * 40)
            
    except FileNotFoundError:
        print("File extracted chưa được tạo. Hãy chạy extract_problem_info() trước.")
    except Exception as e:
        print(f"Lỗi khi preview: {str(e)}")

if __name__ == "__main__":
    print("Bắt đầu extract dữ liệu bài toán...")
    
    success = extract_problem_info()
    
    if success:
        preview_extracted_data()
    
    print("\nHoàn thành!")
