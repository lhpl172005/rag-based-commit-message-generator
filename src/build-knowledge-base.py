# src/build_knowledge_base.py

import faiss
import pickle
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

print("Bắt đầu quá trình xây dựng cơ sở tri thức...")

# 1. Tải và lọc các commit message
print("Đang tải commit messages từ file...")
try:
    with open('data\commit-message.txt', 'r', encoding='utf-8') as f:
        commit_messages = [line for line in f.read().splitlines() if line]
except FileNotFoundError:
    print("LỖI: Không tìm thấy file 'commit_messages.txt' trong thư mục 'data/'.")
    exit()

print(f"Đã tải {len(commit_messages)} commit messages.")

# 2. Tải mô hình Embedding
print("Đang tải mô hình embedding...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Đã tải xong mô hình.")

# 3. Tạo Embeddings
print("Đang tạo embeddings cho các commit...")
embeddings = model.encode(commit_messages, show_progress_bar=True)

# 4. Xây dựng và lưu chỉ mục FAISS
print("Đang xây dựng chỉ mục FAISS...")
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, 'data/faiss-index.bin')
print("Đã lưu chỉ mục FAISS vào file 'data/faiss_index.bin'.")

# 5. Lưu lại các commit message gốc
with open('data/commit-texts.pkl', 'wb') as f:
    pickle.dump(commit_messages, f)
print("Đã lưu các commit message gốc vào file 'data/commit_texts.pkl'.")

print("\nHoàn thành xây dựng cơ sở tri thức!")