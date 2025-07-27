# src/main.py

import sys
import argparse
from pathlib import Path

# Thêm thư mục src vào đường dẫn để có thể import rag_chain
sys.path.append(str(Path(__file__).parent))
from rag_chain import generate_commit_message

def main():
    parser = argparse.ArgumentParser(description="Generate a commit message using RAG.")
    # Thêm 2 cách nhận input: hoặc là từ file, hoặc là trực tiếp từ chuỗi
    parser.add_argument('file', nargs='?', default=None, help="Path to the file containing the git diff.")
    parser.add_argument('--diff', type=str, help="The git diff content as a string.")
    
    args = parser.parse_args()
    diff_content = ""

    if args.diff:
        diff_content = args.diff
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                diff_content = f.read()
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy file tại '{args.file}'")
            return
    else:
        print("Lỗi: Vui lòng cung cấp input là file hoặc chuỗi --diff.")
        parser.print_help()
        return

    if not diff_content.strip():
        print("Lỗi: Nội dung diff rỗng.")
        return

    # Gọi hàm tạo commit message
    generated_message = generate_commit_message(diff_content)
    
    # In kết quả ra để script hook có thể bắt được
    print(generated_message)

if __name__ == '__main__':
    main()