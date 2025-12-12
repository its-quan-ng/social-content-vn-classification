# 🚀 Quick Start - Tiền Xử Lý Dữ Liệu

Hướng dẫn nhanh để bắt đầu tiền xử lý dữ liệu cho PhoBERT.

## 📋 Bước 1: Cài Đặt Dependencies

```bash
# Cài tất cả dependencies
pip install -r requirements.txt

# Hoặc cài từng package cần thiết
pip install pandas numpy pyvi emoji regex openpyxl
```

## ✅ Bước 2: Kiểm Tra Cài Đặt

```bash
# Test xem các module có hoạt động không
python scripts/test_preprocessing.py
```

Nếu thấy `🎉 ALL TESTS PASSED!` là thành công!

## 📂 Bước 3: Chuẩn Bị Dữ Liệu

Đảm bảo bạn có cấu trúc thư mục như sau:

```
data/
├── raw/
│   ├── train_merged.csv    # File train đã merge
│   ├── val.csv             # File validation
│   └── test.csv            # File test
└── processed/
    └── slang_example.csv   # Từ điển slang (đã có)
```

**Format file CSV:**
- Phải có 2 cột: `Sentence` (văn bản) và `Emotion` (nhãn)
- Encoding: UTF-8

## 🔄 Bước 4: Tiền Xử Lý Dữ Liệu

### Option 1: Xử lý tất cả files (RECOMMENDED)

```bash
python scripts/preprocess_data.py \
    --input-dir data/raw \
    --output-dir data/processed \
    --slang-dict data/processed/slang_example.csv
```

### Option 2: Xử lý từng file riêng

```bash
# Train
python scripts/preprocess_data.py \
    --input data/raw/train_merged.csv \
    --output data/processed/train.csv

# Val
python scripts/preprocess_data.py \
    --input data/raw/val.csv \
    --output data/processed/val.csv

# Test
python scripts/preprocess_data.py \
    --input data/raw/test.csv \
    --output data/processed/test.csv
```

## 📊 Bước 5: Kiểm Tra Kết Quả

Sau khi xử lý xong, bạn sẽ có:

```
data/processed/
├── train.csv              # Train data đã xử lý
├── train_stats.txt        # Thống kê train
├── val.csv                # Val data đã xử lý
├── val_stats.txt          # Thống kê val
├── test.csv               # Test data đã xử lý
└── test_stats.txt         # Thống kê test
```

Kiểm tra file stats để xem thống kê:
```bash
cat data/processed/train_stats.txt
```

## 🔍 Bước 6: Xem Kết Quả

```python
import pandas as pd

# Đọc file đã xử lý
df = pd.read_csv('data/processed/train.csv')

# Xem một vài mẫu
print(df[['Sentence', 'Sentence_processed', 'word_count']].head(10))

# Thống kê
print(f"Total rows: {len(df)}")
print(f"Avg words: {df['word_count'].mean():.1f}")
print(f"\nLabel distribution:")
print(df['Emotion'].value_counts())
```

## 💡 Sử Dụng trong Code

### Xử lý 1 câu văn bản

```python
from src.preprocessing import PreprocessingPipeline

# Khởi tạo
pipeline = PreprocessingPipeline(
    slang_dict_path="data/processed/slang_example.csv",
    word_segmentation=True,
    min_word_count=3,
    lowercase=True
)

# Xử lý
text = "Shop này ok lắm 😍 free ship :)) ib shop nhé"
result = pipeline.preprocess(text)
print(result)
# → "cửa_hàng này được lắm thích_thú yêu miễn_phí vận_chuyển cười nhắn tin cửa_hàng nhé"
```

### Xử lý DataFrame

```python
import pandas as pd
from src.preprocessing import PreprocessingPipeline

# Load data
df = pd.read_csv('data/raw/train_merged.csv')

# Khởi tạo pipeline
pipeline = PreprocessingPipeline(
    slang_dict_path="data/processed/slang_example.csv",
    word_segmentation=True,
    min_word_count=3
)

# Xử lý
df_processed = pipeline.preprocess_dataframe(
    df,
    text_column='Sentence',
    output_column='Sentence_processed',
    keep_original=True,
    filter_invalid=True
)

# Lưu
df_processed.to_csv('data/processed/train.csv', index=False, encoding='utf-8-sig')
```

## 🎯 Quy Trình Tiền Xử Lý

Mỗi câu văn bản sẽ đi qua 5 bước:

1. **Text Cleaning** - Loại URL, HTML, mentions, ký tự lặp
2. **Emoji Conversion** - Chuyển emoji sang từ tiếng Việt
3. **Text Normalization** - Chuẩn hóa slang, teencode
4. **Word Segmentation** - Tách từ với PyVi
5. **Final Filtering** - Lọc câu quá ngắn (<3 từ)

**Ví dụ:**
```
Input:  "Shop này okeeee lắm 😍😍 free ship :)) @user"
  ↓ [1. Clean]
Output: "Shop này okee lắm 😍😍 free ship :))"
  ↓ [2. Emoji]
Output: "Shop này okee lắm thích thú yêu thích thú yêu free ship cười"
  ↓ [3. Normalize]
Output: "cửa hàng này được lắm thích thú yêu thích thú yêu miễn phí vận chuyển cười"
  ↓ [4. Segment]
Output: "cửa_hàng này được lắm thích_thú yêu thích_thú yêu miễn_phí vận_chuyển cười"
  ↓ [5. Filter - OK (>3 words)]
Final:  "cửa_hàng này được lắm thích_thú yêu thích_thú yêu miễn_phí vận_chuyển cười"
```

## ⚙️ Tùy Chỉnh

### Thêm slang mới

Chỉnh sửa `data/processed/slang_example.csv`:

```csv
slang,meaning
tqt,tuyệt quá trời
ngon bổ rẻ,chất lượng tốt giá hợp lý
bùi,chất lượng không tốt
fake,giả mạo
auth,chính hãng
```

### Thay đổi config

```bash
python scripts/preprocess_data.py \
    --input data/raw/train.csv \
    --output data/processed/train.csv \
    --min-words 5 \              # Tăng min words
    --no-segmentation            # Tắt word segmentation
```

## 🐛 Troubleshooting

### Lỗi: PyVi not found
```bash
pip install pyvi
```

### Lỗi: Encoding error
Đảm bảo file CSV dùng UTF-8:
```python
df.to_csv('file.csv', encoding='utf-8-sig', index=False)
```

### Lỗi: Column not found
Kiểm tra tên cột trong CSV:
```python
df = pd.read_csv('data.csv')
print(df.columns)
```

## 📚 Tài Liệu Chi Tiết

- [PREPROCESSING_GUIDE.md](PREPROCESSING_GUIDE.md) - Hướng dẫn chi tiết
- [src/preprocessing/README.md](src/preprocessing/README.md) - API documentation
- [README.md](README.md) - Project overview

## ✅ Checklist

- [ ] Cài đặt dependencies: `pip install -r requirements.txt`
- [ ] Test hoạt động: `python scripts/test_preprocessing.py`
- [ ] Chuẩn bị dữ liệu: Files CSV trong `data/raw/`
- [ ] Chạy preprocessing: `python scripts/preprocess_data.py`
- [ ] Kiểm tra output: Files trong `data/processed/`
- [ ] Xem thống kê: Đọc files `*_stats.txt`

## 🎉 Hoàn Thành!

Bây giờ bạn đã có dữ liệu sạch và sẵn sàng cho fine-tuning PhoBERT!

**Bước tiếp theo:**
- Fine-tune PhoBERT với dữ liệu đã xử lý
- Đánh giá model trên test set
- So sánh với baseline (SVM, Naive Bayes)

---

**Nếu cần trợ giúp, hãy tham khảo:**
- [PREPROCESSING_GUIDE.md](PREPROCESSING_GUIDE.md)
- [Issues trên GitHub](https://github.com/...)

