"""
Corpus Statistics Analysis
Phân tích thống kê ngữ liệu trước khi tiền xử lý
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from collections import Counter

# Setup
plt.rcParams['font.family'] = 'DejaVu Sans'
sns.set_style("whitegrid")

DATA_DIR = Path(__file__).parent.parent / "data" / "raw"
OUTPUT_DIR = Path(__file__).parent.parent / "report"
OUTPUT_DIR.mkdir(exist_ok=True)

# Đọc dữ liệu
print("📂 Loading data...")
df_train = pd.read_csv(DATA_DIR / "train_merged.csv")
df_val = pd.read_csv(DATA_DIR / "val.csv")
df_test = pd.read_csv(DATA_DIR / "test.csv")

print(f"✓ Train: {len(df_train)} samples")
print(f"✓ Val: {len(df_val)} samples")
print(f"✓ Test: {len(df_test)} samples")

# Thống kê tổng quát
total = len(df_train) + len(df_val) + len(df_test)

# Thống kê độ dài câu
def get_length_stats(df):
    lengths = df['Sentence'].str.split().str.len()
    return {
        'mean': lengths.mean(),
        'std': lengths.std(),
        'min': lengths.min(),
        'max': lengths.max(),
        'median': lengths.median()
    }

train_len = get_length_stats(df_train)
val_len = get_length_stats(df_val)
test_len = get_length_stats(df_test)

# Thống kê phân bố độ dài theo khoảng và emotion
def get_length_distribution_by_emotion(df):
    df['length'] = df['Sentence'].str.split().str.len()
    
    # Định nghĩa các khoảng độ dài
    bins = [0, 5, 10, 15, 20, 25, 30, float('inf')]
    labels = ['1-5', '6-10', '10-15', '16-20', '21-25', '26-30', '>30']
    
    df['length_bin'] = pd.cut(df['length'], bins=bins, labels=labels, right=True)
    
    # Tạo bảng pivot: length_bin x emotion
    pivot_table = pd.crosstab(df['length_bin'], df['Emotion'], normalize='all') * 100
    
    # Thêm cột Overall (tổng theo hàng)
    pivot_table['Overall'] = pivot_table.sum(axis=1)
    
    return pivot_table

length_emotion_dist = get_length_distribution_by_emotion(df_train)

# Thống kê vocab
all_text = ' '.join(df_train['Sentence'].tolist())
words = all_text.lower().split()
vocab_size = len(set(words))
total_words = len(words)

# Thống kê nhãn
emotion_counts_train = df_train['Emotion'].value_counts().sort_index()
emotion_counts_val = df_val['Emotion'].value_counts().sort_index()
emotion_counts_test = df_test['Emotion'].value_counts().sort_index()

# Class imbalance ratio
max_class = emotion_counts_train.max()
min_class = emotion_counts_train.min()
imbalance_ratio = max_class / min_class

# ============= XUẤT KẾT QUẢ =============

output = f"""# Corpus Statistics Report
Generated before preprocessing

## 1. Dataset Overview

| Split | Samples | Percentage |
|-------|---------|------------|
| Train | {len(df_train):,} | {len(df_train)/total*100:.1f}% |
| Validation | {len(df_val):,} | {len(df_val)/total*100:.1f}% |
| Test | {len(df_test):,} | {len(df_test)/total*100:.1f}% |
| **Total** | **{total:,}** | **100%** |

## 2. Emotion Label Distribution

### Train Set
| Emotion | Sentences | Percentage |
|---------|-----------|------------|
"""

for emotion, count in emotion_counts_train.items():
    output += f"| {emotion} | {count:,} | {count/len(df_train)*100:.2f}% |\n"

output += f"""| **Total** | **{len(df_train):,}** | **100%** |

**Class Imbalance Ratio**: {imbalance_ratio:.2f} (Most frequent / Least frequent)

### Validation Set
| Emotion | Sentences | Percentage |
|---------|-----------|------------|
"""

for emotion, count in emotion_counts_val.items():
    output += f"| {emotion} | {count:,} | {count/len(df_val)*100:.2f}% |\n"

output += f"""
### Test Set
| Emotion | Sentences | Percentage |
|---------|-----------|------------|
"""

for emotion, count in emotion_counts_test.items():
    output += f"| {emotion} | {count:,} | {count/len(df_test)*100:.2f}% |\n"

output += f"""
## 3. Sentence Length Statistics

### 3.1 Basic Statistics

| Metric | Train | Val | Test |
|--------|-------|-----|------|
| Mean | {train_len['mean']:.2f} | {val_len['mean']:.2f} | {test_len['mean']:.2f} |
| Std Dev | {train_len['std']:.2f} | {val_len['std']:.2f} | {test_len['std']:.2f} |
| Min | {int(train_len['min'])} | {int(val_len['min'])} | {int(test_len['min'])} |
| Max | {int(train_len['max'])} | {int(val_len['max'])} | {int(test_len['max'])} |
| Median | {train_len['median']:.1f} | {val_len['median']:.1f} | {test_len['median']:.1f} |

### 3.2 Length Distribution by Emotion (Train Set)

Distribution of sentence lengths across different emotions (percentage of total dataset):

| Length | """

# Thêm header cho các cột emotion
for emotion in length_emotion_dist.columns:
    output += f"{emotion} | "

output += "\n|" + "--------|" * (len(length_emotion_dist.columns) + 1) + "\n"

# Thêm từng hàng dữ liệu
for length_bin in length_emotion_dist.index:
    output += f"| {length_bin} | "
    for emotion in length_emotion_dist.columns:
        output += f"{length_emotion_dist.loc[length_bin, emotion]:.2f} | "
    output += "\n"

# Thêm hàng Total
output += "| **Total** | "
for emotion in length_emotion_dist.columns:
    output += f"**{length_emotion_dist[emotion].sum():.2f}** | "
output += "\n"

output += f"""
**Observations**:
- Most sentences fall in the 6-10 and 10-15 word ranges
- Very short (1-5) and very long (>30) sentences are less common
- Emotion distribution varies across length ranges

## 4. Vocabulary Statistics (Train set)

| Metric | Value |
|--------|-------|
| Total words (tokens) | {total_words:,} |
| Unique words (vocab) | {vocab_size:,} |
| Vocab richness | {vocab_size/total_words*100:.2f}% |

## 5. Data Quality Notes

- **Source**: UIT-VSMEC (train/val/test) + Self-collected comments (merged into train)
- **Language**: Vietnamese (social media text)
- **Preprocessing status**: Raw data (before normalization and word segmentation)
- **Class distribution**: Imbalanced - Enjoyment is most frequent, Surprise is least frequent
"""

# Lưu file
report_path = OUTPUT_DIR / "corpus_statistics.md"
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(output)

print(f"\n✓ Report saved to: {report_path}")

# ============= VẼ BIỂU ĐỒ =============

print("\n📊 Generating visualizations...")

# 1a. Emotion distribution - Bar chart
fig, ax = plt.subplots(figsize=(10, 6))
emotion_counts_train.plot(kind='bar', ax=ax, color='steelblue')
ax.set_title('Emotion Distribution (Train Set)', fontsize=14, fontweight='bold')
ax.set_xlabel('Emotion', fontsize=12)
ax.set_ylabel('Count', fontsize=12)
ax.tick_params(axis='x', rotation=45)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "emotion_distribution_bar.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: emotion_distribution_bar.png")

# 1b. Emotion distribution - Pie chart
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(emotion_counts_train, labels=emotion_counts_train.index, autopct='%1.1f%%', 
       startangle=90, colors=sns.color_palette("husl", len(emotion_counts_train)))
ax.set_title('Emotion Percentage (Train Set)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "emotion_distribution_pie.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: emotion_distribution_pie.png")

# 2. Length distribution - Histogram
fig, ax = plt.subplots(figsize=(10, 6))
train_lengths = df_train['Sentence'].str.split().str.len()
ax.hist(train_lengths, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
ax.axvline(train_lengths.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {train_lengths.mean():.1f}')
ax.axvline(train_lengths.median(), color='green', linestyle='--', linewidth=2, label=f'Median: {train_lengths.median():.1f}')
ax.set_title('Sentence Length Distribution (Train Set)', fontsize=14, fontweight='bold')
ax.set_xlabel('Number of Words', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_xlim(0, 100)  # Giới hạn trục lại 
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "length_distribution.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: length_distribution.png")

# 2b. Length distribution by emotion - Heatmap
fig, ax = plt.subplots(figsize=(12, 6))
# Loại bỏ cột Overall cho heatmap để tập trung vào emotions
heatmap_data = length_emotion_dist.drop('Overall', axis=1)
sns.heatmap(heatmap_data, annot=True, fmt='.2f', cmap='YlOrRd', 
            cbar_kws={'label': 'Percentage (%)'}, ax=ax, linewidths=0.5)
ax.set_title('Sentence Length Distribution by Emotion (Train Set)', fontsize=14, fontweight='bold')
ax.set_xlabel('Emotion', fontsize=12)
ax.set_ylabel('Sentence Length Range', fontsize=12)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "length_emotion_heatmap.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: length_emotion_heatmap.png")

# 3. Dataset split comparison
fig, ax = plt.subplots(figsize=(8, 6))
splits = ['Train', 'Val', 'Test']
counts = [len(df_train), len(df_val), len(df_test)]
colors = ['#3498db', '#2ecc71', '#e74c3c']
ax.bar(splits, counts, color=colors, edgecolor='black', linewidth=1.5)
ax.set_title('Dataset Split Distribution', fontsize=14, fontweight='bold')
ax.set_ylabel('Number of Samples', fontsize=12)
for i, (split, count) in enumerate(zip(splits, counts)):
    ax.text(i, count + 100, f'{count:,}\n({count/total*100:.1f}%)', 
            ha='center', va='bottom', fontsize=11, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "dataset_splits.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: dataset_splits.png")

print("\n✅ Analysis complete!")
print(f"📁 Check report/ directory for results")

