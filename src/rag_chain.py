# src/rag_chain.py

import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Tải các biến môi trường (chứa API key) từ file .env
load_dotenv()

# --- Lớp Retriever (Giống như bước trước) ---
class CommitRetriever:
    def __init__(self, index_path, texts_path, model_name='all-MiniLM-L6-v2'):
        print("Đang tải cơ sở tri thức...")
        self.index = faiss.read_index(index_path)
        with open(texts_path, 'rb') as f:
            self.texts = pickle.load(f)
        self.model = SentenceTransformer(model_name)
        print("Retriever đã sẵn sàng!")

    def retrieve(self, query: str, k: int = 5):
        query_embedding = self.model.encode([query])
        _, indices = self.index.search(query_embedding, k)
        return [self.texts[i] for i in indices[0]]

# --- Hàm chính để tạo commit message ---
def generate_commit_message(diff_content: str):
    # 1. Khởi tạo Retriever
    retriever = CommitRetriever(
        index_path='data/faiss-index.bin',
        texts_path='data/commit-texts.pkl'
    )
    
    # 2. Dùng Retriever để tìm các ví dụ liên quan
    print("Đang tìm kiếm các commit tương tự...")
    retrieved_examples = retriever.retrieve(diff_content, k=5)
    
    # Định dạng lại các ví dụ để đưa vào prompt
    formatted_examples = "\n---\n".join([f"Ví dụ {i+1}:\n{example}" for i, example in enumerate(retrieved_examples)])
    
    # 3. Tạo Prompt Template
    prompt_template = f"""
    Bạn là một chuyên gia lập trình. Nhiệm vụ của bạn là viết một commit message ngắn gọn, chuyên nghiệp theo chuẩn Conventional Commits.

    Dưới đây là các thay đổi trong code (git diff) và một vài ví dụ về các commit message tốt trong quá khứ có nội dung tương tự.

    **HƯỚNG DẪN:**
    - Commit message phải bắt đầu bằng một loại commit (ví dụ: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`).
    - Viết bằng tiếng Anh.
    - Phần mô tả phải ngắn gọn, tập trung vào "cái gì" và "tại sao" đã thay đổi.

    **CÁC VÍ DỤ THAM KHẢO:**
    {formatted_examples}

    **CÁC THAY ĐỔI TRONG CODE CẦN TẠO COMMIT (GIT DIFF):**
    ```diff
    {diff_content}
    ```

    **COMMIT MESSAGE ĐƯỢC TẠO RA:**
    """
    
    # 4. Gọi Gemini để tạo commit
    print("Đang gửi yêu cầu tới Gemini...")
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)
    
    # Gửi toàn bộ prompt tới Gemini
    response = llm.invoke(prompt_template)
    
    print("Đã nhận được kết quả!")
    return response.content

# --- Phần này để chạy thử nghiệm file ---
if __name__ == '__main__':
    try:
        # Đọc nội dung từ một file diff mẫu
        with open('my-changes.txt', 'r', encoding='utf-8') as f:
            sample_diff = f.read()
        
        # Tạo commit message
        generated_message = generate_commit_message(sample_diff)
        
        print("\n===================================")
        print("🤖 COMMIT MESSAGE ĐƯỢC TẠO TỰ ĐỘNG:")
        print("===================================")
        print(generated_message)

    except FileNotFoundError:
        print("\nLỖI: Không tìm thấy file 'my-changes.txt' ở thư mục gốc.")
        print("Hãy tạo một file tên là 'my-changes.txt', dán nội dung 'git diff' của bạn vào đó và chạy lại.")