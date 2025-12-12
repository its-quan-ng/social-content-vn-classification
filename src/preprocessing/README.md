## 📦 Preprocessing Module

Module tiền xử lý văn bản tiếng Việt cho PhoBERT Sentiment Analysis.

### 🎯 Tính Năng

- **TextCleaner**: Làm sạch văn bản (URL, HTML, mentions, ký tự lặp, v.v.)
- **EmojiHandler**: Chuyển đổi emoji và emoticons sang tiếng Việt
- **TextNormalizer**: Chuẩn hóa slang, teencode, viết tắt
- **WordSegmenter**: Tách từ tiếng Việt (PyVi, VnCoreNLP)
- **PreprocessingPipeline**: Pipeline tích hợp tất cả các bước

### 🚀 Cài Đặt

```bash
# Cài các dependencies cơ bản
pip install pandas numpy emoji regex

# Cài PyVi cho word segmentation (RECOMMENDED)
pip install pyvi

# Hoặc VnCoreNLP (cần Java)
pip install vncorenlp
```

### 📖 Sử Dụng

#### 1. Sử dụng module riêng lẻ

```python
from src.preprocessing import TextCleaner, EmojiHandler, TextNormalizer

# Text Cleaner
cleaner = TextCleaner()
text = "Shop này okeeee lắm 😍 @user https://abc.com"
cleaned = cleaner.clean(text)
# → "Shop này okee lắm 😍"

# Emoji Handler
handler = EmojiHandler()
text = "Sản phẩm đẹp quá 😍😍 :))"
converted = handler.convert(text)
# → "Sản phẩm đẹp quá thích thú yêuthích thú yêu cười"

# Text Normalizer
normalizer = TextNormalizer()
text = "Sp này ok lắm m thích"
normalized = normalizer.normalize(text)
# → "sản phẩm này được lắm mình thích"
```

#### 2. Sử dụng Pipeline (RECOMMENDED)

```python
from src.preprocessing import PreprocessingPipeline

# Khởi tạo pipeline
pipeline = PreprocessingPipeline(
    slang_dict_path="data/processed/slang_example.csv",
    word_segmentation=True,
    min_word_count=3,
    lowercase=True
)

# Xử lý 1 văn bản
text = "Shop này ok lắm 😍 free ship :)) @user"
result = pipeline.preprocess(text)
# → "cửa_hàng này được lắm thích_thú yêu miễn_phí vận_chuyển cười"

# Xử lý nhiều văn bản
texts = ["Sp tốt", "Dịch vụ tệ", "Giao hàng nhanh"]
results = pipeline.preprocess_batch(texts)

# Xử lý DataFrame
import pandas as pd
df = pd.read_csv("data.csv")
df_processed = pipeline.preprocess_dataframe(
    df,
    text_column='Sentence',
    output_column='Sentence_processed'
)
```

#### 3. Xử lý toàn bộ dataset

```bash
# Xử lý 1 file
python scripts/preprocess_data.py \
    --input data/raw/train.csv \
    --output data/processed/train.csv

# Xử lý tất cả train/val/test
python scripts/preprocess_data.py \
    --input-dir data/raw \
    --output-dir data/processed \
    --slang-dict data/processed/slang_example.csv
```

### 🧪 Testing

```bash
# Chạy tests
python scripts/test_preprocessing.py

# Demo các module
python src/preprocessing/text_cleaner.py
python src/preprocessing/emoji_handler.py
python src/preprocessing/text_normalizer.py
python src/preprocessing/word_segmenter.py
python src/preprocessing/preprocessing_pipeline.py
```

### 📊 Quy Trình Xử Lý

```
Input Text
    ↓
1. Text Cleaning
   • Loại URL, email, phone
   • Loại HTML, mentions, hashtags
   • Rút gọn ký tự lặp
    ↓
2. Emoji Conversion
   • 😍 → "thích thú yêu"
   • :)) → "cười"
    ↓
3. Text Normalization
   • Slang: "sp" → "sản phẩm"
   • Teencode: "ko" → "không"
    ↓
4. Word Segmentation (PyVi)
   • "sản phẩm tốt" → "sản_phẩm tốt"
    ↓
5. Final Cleanup
   • Lowercase
   • Filter (min 3 words)
    ↓
Output: Clean Text
```

### ⚙️ Configuration

```python
pipeline = PreprocessingPipeline(
    slang_dict_path=None,              # Path to slang dictionary
    word_segmentation=True,            # Enable word segmentation
    segmentation_method='pyvi',        # 'pyvi', 'vncorenlp', 'simple'
    vncorenlp_path=None,              # VnCoreNLP jar path
    min_word_count=3,                  # Minimum words after segmentation
    lowercase=True                     # Convert to lowercase
)
```

### 📝 Thêm Slang Mới

Thêm vào file `data/processed/slang_example.csv`:

```csv
slang,meaning
tqt,tuyệt quá trời
ngon bổ rẻ,chất lượng tốt giá hợp lý
bùi,chất lượng không tốt
```

### 🔧 Troubleshooting

**PyVi not found:**
```bash
pip install pyvi
```

**VnCoreNLP not working:**
- Cần cài Java JRE >= 1.8
- Download VnCoreNLP: https://github.com/vncorenlp/VnCoreNLP
- Cung cấp path đến jar file

**Encoding errors:**
- Đảm bảo file CSV dùng UTF-8
- Dùng `encoding='utf-8-sig'` khi đọc CSV

### 📚 Tài Liệu

- [PREPROCESSING_GUIDE.md](../../PREPROCESSING_GUIDE.md) - Hướng dẫn chi tiết
- [PhoBERT Paper](https://arxiv.org/abs/2003.00744)
- [PyVi GitHub](https://github.com/trungtv/pyvi)
- [VnCoreNLP GitHub](https://github.com/vncorenlp/VnCoreNLP)

### 🆘 Hỗ Trợ

Nếu gặp vấn đề:
1. Chạy `python scripts/test_preprocessing.py` để kiểm tra
2. Kiểm tra encoding của files (UTF-8)
3. Đảm bảo đã cài đủ dependencies: `pip install -r requirements.txt`

---

**Version**: 1.0.0  
**Author**: PPNCKH Project

