# 📋 Hướng Dẫn Tiền Xử Lý Dữ Liệu - PhoBERT Sentiment Analysis

## 🎯 Tổng Quan Quy Trình

### Quy trình đề xuất cho đồ án của bạn:

```
┌─────────────────────────────────────────────────────────────┐
│                    1. CHUẨN BỊ DỮ LIỆU                      │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┴─────────────────────┐
        │                                           │
        ▼                                           ▼
┌───────────────────┐                   ┌───────────────────┐
│ DỮ LIỆU TỰ THU   │                   │  DỮ LIỆU UIT      │
│ THẬP (1.5k x 3)   │                   │  (train/val/test) │
└───────────────────┘                   └───────────────────┘
        │                                           │
        ▼                                           │
┌───────────────────┐                               │
│ BƯỚC 1:           │                               │
│ Gộp 3 file → 1    │                               │
└───────────────────┘                               │
        │                                           │
        ▼                                           │
┌───────────────────┐                               │
│ BƯỚC 2:           │                               │
│ Gán nhãn cảm xúc  │                               │
│ (7 nhãn)          │                               │
└───────────────────┘                               │
        │                                           │
        │                    ┌────────────────────────┘
        │                    │
        ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                  2. TIỀN XỬ LÝ VĂN BẢN                      │
│  • Làm sạch (URL, HTML, mentions, hashtags)                │
│  • Chuyển emoji → text tiếng Việt                          │
│  • Chuẩn hóa teencode/slang                                │
│  • Chuẩn hóa dấu câu, ký tự lặp                            │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│              3. CHIA TẬP TRAIN/VAL/TEST                     │
│  • UIT: Giữ nguyên train/val/test đã có                    │
│  • Tự thu thập: Chia 80/10/10                              │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│           4. KẾT HỢP DỮ LIỆU (TÙY CHỌN)                     │
│  • Gộp TRAIN của UIT + TRAIN tự thu thập                   │
│  • ⚠️ KHÔNG gộp val/test                                    │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│               5. FINE-TUNE PHOBERT                          │
└─────────────────────────────────────────────────────────────┘
```

---

## ❓ Câu Hỏi Của Bạn - Trả Lời Chi Tiết

### 1️⃣ "Có nên gộp 3 file 1.5k comments thành 1 không?"

**✅ Có, NÊN gộp.**

**Lý do:**
- Dễ quản lý: 1 file thay vì 3 file
- Dễ gán nhãn: Gán nhãn tập trung
- Dễ chia train/val/test: Chia đều và balanced

**Cách làm:**
```python
from src.data_processing.merge_collected_data import merge_collected_files

merged_df = merge_collected_files(
    input_files=[
        "data/raw/collected_1.xlsx",
        "data/raw/collected_2.xlsx", 
        "data/raw/collected_3.xlsx"
    ],
    output_file="data/raw/merged_collected.csv",
    label_column='label'
)
```

### 2️⃣ "Có nên gộp 3 file của UIT làm 1 không?"

**❌ KHÔNG, KHÔNG NÊN gộp.**

**Lý do:**
- UIT đã chia sẵn train/val/test một cách khoa học
- Nếu gộp lại sẽ:
  - ❌ Mất phân chia chuẩn
  - ❌ Có thể gây **data leakage** (test data lọt vào training)
  - ❌ Không so sánh được với các nghiên cứu khác (họ dùng test set chuẩn)

**Cách làm ĐÚNG:**
```python
from src.data_processing.process_uit_data import load_uit_data, preprocess_uit_data

# Load và GIỮ NGUYÊN cấu trúc
train_df, val_df, test_df = load_uit_data(
    train_file="data/raw/uit/train.csv",
    val_file="data/raw/uit/dev.csv",
    test_file="data/raw/uit/test.csv"
)

# Tiền xử lý RIÊNG từng file
train_processed, val_processed, test_processed = preprocess_uit_data(
    train_df, val_df, test_df,
    output_dir="data/processed/uit"
)
```

### 3️⃣ "Gộp emoji, slang, viết tắt làm 1 hay tách riêng?"

**✅ Tách riêng nhưng ghép thành 1 pipeline.**

**Lý do:**
- **Tách riêng** giúp:
  - Dễ debug và sửa lỗi
  - Dễ bật/tắt từng module
  - Dễ mở rộng và maintain code
  - Có thể test độc lập

- **Ghép pipeline** giúp:
  - Dễ sử dụng (1 lần gọi là xong)
  - Thứ tự xử lý đúng
  - Performance tốt hơn

**Code đã tạo sẵn:**
```python
from src.preprocessing.preprocessing_pipeline import PreprocessingPipeline

# Pipeline tích hợp tất cả
pipeline = PreprocessingPipeline(
    slang_dict_path="data/processed/slang_example.csv"
)

# Xử lý 1 dòng
text = "Sp này đẹpppp 😍😍 m thích lắm, ib cho shop nha :)))"
processed = pipeline.preprocess(text)
# → "sản phẩm này đẹp thích thú yêu thích thú yêu mình thích lắm nhắn tin cho shop nhé cười"
```

---

## 🚀 Bắt Đầu Nhanh

### Bước 1: Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### Bước 2: Chuẩn bị dữ liệu

**Cấu trúc thư mục:**
```
data/
├── raw/
│   ├── collected_1.xlsx    # Dữ liệu tự thu thập
│   ├── collected_2.xlsx
│   ├── collected_3.xlsx
│   └── uit/
│       ├── train.csv       # Dữ liệu UIT
│       ├── dev.csv
│       └── test.csv
└── processed/
    └── slang_example.csv   # Từ điển slang (đã có)
```

### Bước 3: Chạy demo

```bash
# Test preprocessing pipeline
python src/preprocessing/preprocessing_pipeline.py

# Test emoji handler
python src/preprocessing/emoji_handler.py

# Test text normalizer
python src/preprocessing/text_normalizer.py
```

### Bước 4: Xử lý dữ liệu thực tế

**Script hoàn chỉnh:**

```python
# scripts/process_all_data.py
from pathlib import Path
from src.data_processing.merge_collected_data import merge_collected_files, split_train_val_test
from src.data_processing.process_uit_data import load_uit_data, preprocess_uit_data
import pandas as pd

project_root = Path(__file__).parent.parent

# ===== 1. XỬ LÝ DỮ LIỆU TỰ THU THẬP =====
print("=" * 60)
print("PHẦN 1: XỬ LÝ DỮ LIỆU TỰ THU THẬP")
print("=" * 60)

# Gộp 3 files
collected_files = [
    project_root / "data/raw/collected_1.xlsx",
    project_root / "data/raw/collected_2.xlsx",
    project_root / "data/raw/collected_3.xlsx",
]

merged_df = merge_collected_files(
    input_files=collected_files,
    output_file=project_root / "data/raw/merged_collected.csv"
)

# ⚠️ SAU BƯỚC NÀY: GÁN NHÃN THỦ CÔNG CHO merged_collected.csv

# Sau khi gán nhãn xong:
# merged_df = pd.read_csv("data/raw/merged_collected_labeled.csv")
# train, val, test = split_train_val_test(
#     df=merged_df,
#     output_dir=project_root / "data/processed/collected"
# )

# ===== 2. XỬ LÝ DỮ LIỆU UIT =====
print("\n" + "=" * 60)
print("PHẦN 2: XỬ LÝ DỮ LIỆU UIT-VSMEC")
print("=" * 60)

# Load UIT data
train_uit, val_uit, test_uit = load_uit_data(
    train_file=project_root / "data/raw/uit/train.csv",
    val_file=project_root / "data/raw/uit/dev.csv",
    test_file=project_root / "data/raw/uit/test.csv"
)

# Tiền xử lý
train_uit, val_uit, test_uit = preprocess_uit_data(
    train_df=train_uit,
    val_df=val_uit,
    test_df=test_uit,
    slang_dict_path=project_root / "data/processed/slang_example.csv",
    output_dir=project_root / "data/processed/uit"
)

# ===== 3. KẾT HỢP DỮ LIỆU (SAU KHI ĐÃ CÓ NHÃN) =====
print("\n" + "=" * 60)
print("PHẦN 3: KẾT HỢP DỮ LIỆU TRAIN")
print("=" * 60)

# Chỉ gộp train sets
# train_collected = pd.read_csv("data/processed/collected/train.csv")
# train_combined = pd.concat([train_uit, train_collected], ignore_index=True)
# train_combined = train_combined.sample(frac=1, random_state=42).reset_index(drop=True)
# train_combined.to_csv("data/processed/combined/train.csv", index=False)

print("\n✓ HOÀN THÀNH TIỀN XỬ LÝ DỮ LIỆU!")
```

---

## 📊 Thống Kê Dữ Liệu Dự Kiến

Theo kế hoạch đồ án của bạn:

| Nguồn | Số mẫu | Train (80%) | Val (10%) | Test (10%) |
|-------|--------|-------------|-----------|------------|
| **UIT-VSMEC** | ~6,927 | ~5,541 | ~693 | ~693 |
| **Tự thu thập** | ~4,500 (1.5k×3) | ~3,600 | ~450 | ~450 |
| **Tổng cộng** | **~11,427** | **~9,141** | **~1,143** | **~1,143** |

**Lưu ý:** Số liệu cuối cùng phụ thuộc vào:
- Số mẫu duplicate bị loại bỏ
- Số mẫu có text rỗng sau tiền xử lý

---

## ⚙️ Tùy Chỉnh Pipeline

### Tùy chỉnh slang dictionary

Bổ sung vào `data/processed/slang_example.csv`:

```csv
slang,meaning
tqt,tuyệt quá trời
ngon bổ rẻ,chất lượng tốt giá hợp lý
bùi,chất lượng không tốt
fake,giả mạo
auth,chính hãng
ship,vận chuyển
cod,thu tiền khi giao hàng
```

### Tùy chỉnh pipeline parameters

```python
pipeline = PreprocessingPipeline(
    slang_dict_path="data/processed/slang_example.csv",
    remove_numbers=False,      # Giữ số (VD: "5 sao", "100k")
    keep_vietnamese=True,      # Giữ dấu tiếng Việt
    remove_stopwords=False     # KHÔNG remove cho BERT
)
```

---

## 📌 Lưu Ý Quan Trọng

### ✅ NÊN:
1. **Gộp** 3 file tự thu thập thành 1
2. **GIỮ NGUYÊN** train/val/test của UIT
3. **Tiền xử lý** cả 2 nguồn dữ liệu
4. **Kiểm tra** chất lượng sau tiền xử lý
5. **Lưu** bản gốc trước khi xử lý (cột `text_original`)
6. **Sử dụng** random seed để reproducible

### ❌ KHÔNG NÊN:
1. **Gộp** train/val/test của UIT thành 1 file
2. **Thêm** dữ liệu tự thu thập vào val/test của UIT
3. **Loại bỏ** emoji hoàn toàn (chuyển thành text thay vì xóa)
4. **Remove stopwords** khi dùng PhoBERT
5. **Stemming/Lemmatization** (không cần thiết cho Transformer)
6. **Mất dấu** tiếng Việt

---

## 🔄 Quy Trình Làm Việc Đề Xuất

### Giai đoạn 1: Chuẩn bị (Đang làm)
- [x] Tạo cấu trúc code tiền xử lý
- [ ] Gộp 3 file tự thu thập
- [ ] **Gán nhãn cho dữ liệu tự thu thập** ⚠️ Quan trọng
- [ ] Chia train/val/test cho dữ liệu tự thu thập

### Giai đoạn 2: Tiền xử lý
- [ ] Tiền xử lý UIT-VSMEC
- [ ] Tiền xử lý dữ liệu tự thu thập
- [ ] Kiểm tra chất lượng dữ liệu
- [ ] Phân tích thống kê

### Giai đoạn 3: Fine-tune PhoBERT
- [ ] Setup môi trường training
- [ ] Thử nghiệm trên UIT only
- [ ] Thử nghiệm trên combined data
- [ ] So sánh kết quả

### Giai đoạn 4: Đánh giá
- [ ] Đánh giá trên test set
- [ ] Phân tích confusion matrix
- [ ] So sánh với baseline (SVM)

---

## 💡 Tips & Tricks

### Gán nhãn hiệu quả
- Dùng **Label Studio** (free, open-source): https://labelstud.io/
- Hoặc tạo Google Sheets với dropdown list cho 7 nhãn
- Nên có 2-3 người gán độc lập để tính Inter-Annotator Agreement (IAA)

### Xử lý class imbalance
```python
from sklearn.utils.class_weight import compute_class_weight

# Tính class weights
class_weights = compute_class_weight(
    'balanced',
    classes=train_df['label'].unique(),
    y=train_df['label']
)
```

### Data Augmentation (nếu cần)
- Back-translation (Việt → Anh → Việt)
- Synonym replacement (thay từ đồng nghĩa)
- Random deletion (xóa ngẫu nhiên 1-2 từ)

---

## 📚 Tài Liệu Tham Khảo

- **PhoBERT paper**: https://arxiv.org/abs/2003.00744
- **UIT-VSMEC dataset**: https://github.com/vihung169/VietnameseSentimentAnalysis
- **Hugging Face Transformers**: https://huggingface.co/docs/transformers

---

## 🆘 Hỗ Trợ

Nếu gặp vấn đề, kiểm tra:
1. `src/data_processing/README.md` - Hướng dẫn chi tiết
2. Chạy test scripts trong các module
3. Kiểm tra encoding của file (UTF-8)
4. Đảm bảo đã cài đủ dependencies

---

**Chúc bạn thành công với đồ án! 🎓🚀**


