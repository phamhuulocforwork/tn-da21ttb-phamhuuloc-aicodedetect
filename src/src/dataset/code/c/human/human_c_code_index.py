import os
import pandas as pd

def scan_human_c_code(base_path="dataset/c/human"):
    data = []
    for problem_id in os.listdir(base_path):
        problem_path = os.path.join(base_path, problem_id)
        if not os.path.isdir(problem_path):
            continue
        for file in os.listdir(problem_path):
            if file.endswith(".cpp"):
                filepath = os.path.join(problem_path, file)
                data.append({
                    "filename": file,
                    "filepath": filepath,
                    "problem_id": problem_id,
                    "author_type": "human",
                    "language": "C"
                })
    return pd.DataFrame(data)

# Gọi hàm
df = scan_human_c_code()

# Lưu thành CSV để xử lý tiếp
df.to_csv("human_c_code_index.csv", index=False)
print("✅ Đã lưu thông tin file vào human_c_code_index.csv")
