"""
Clean emotion labels - fix typos and standardize
"""
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "raw"

# Đọc file
print("📂 Loading train_merged.csv...")
df = pd.read_csv(DATA_DIR / "train_merged.csv")

print(f"Total samples: {len(df)}")
print(f"\n🔍 Unique labels BEFORE cleaning:")
print(df['Emotion'].value_counts().sort_index())

# Map các nhãn sai về đúng
label_mapping = {
    # Chuẩn (giữ nguyên)
    'Enjoyment': 'Enjoyment',
    'Sadness': 'Sadness',
    'Anger': 'Anger',
    'Disgust': 'Disgust',
    'Fear': 'Fear',
    'Surprise': 'Surprise',
    'Other': 'Other',
    
    # Sai chính tả / viết thường / khoảng trắng
    'sadness': 'Sadness',
    'Ther': 'Other',
    'Ager': 'Anger',
    'DIsgust': 'Disgust',
    'Disgut': 'Disgust',
    'ENjoyment': 'Enjoyment',
    'Fera': 'Fear',
    'Othher': 'Other',
    'Ptjer': 'Other',  # typo của Other
    'Suprise': 'Surprise',
    'Ẹnjoyment': 'Enjoyment',  # lỗi font
    'FearEnjoyment': 'Fear',  # gán về Fear (hoặc có thể bỏ)
    
    # Có khoảng trắng thừa
    'Disgust ': 'Disgust',
    'Enjoyment ': 'Enjoyment',
    'Fear ': 'Fear',
    'Other ': 'Other',
    'Sadness ': 'Sadness',
}

# Xử lý: strip khoảng trắng trước, rồi map
df['Emotion'] = df['Emotion'].str.strip()  # Xóa khoảng trắng 2 bên
df['Emotion'] = df['Emotion'].map(label_mapping)

# Kiểm tra có nhãn nào không map được không
unmapped = df[df['Emotion'].isna()]
if len(unmapped) > 0:
    print(f"\n⚠️ WARNING: {len(unmapped)} samples with unmapped labels!")
    print(unmapped[['id', 'Emotion', 'Sentence']].head())
else:
    print("\n✅ All labels mapped successfully!")

print(f"\n🔍 Unique labels AFTER cleaning:")
print(df['Emotion'].value_counts().sort_index())

# Lưu lại file
df.to_csv(DATA_DIR / "train_merged.csv", index=False, encoding="utf-8-sig")
print(f"\n✅ Saved cleaned file to: train_merged.csv")

# Thống kê
print("\n📊 Label distribution:")
for emotion, count in df['Emotion'].value_counts().sort_index().items():
    print(f"  {emotion}: {count:,} ({count/len(df)*100:.2f}%)")

