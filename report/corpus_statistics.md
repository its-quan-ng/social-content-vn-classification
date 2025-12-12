# Corpus Statistics Report
Generated before preprocessing

## 1. Dataset Overview

| Split | Samples | Percentage |
|-------|---------|------------|
| Train | 11,472 | 89.3% |
| Validation | 686 | 5.3% |
| Test | 693 | 5.4% |
| **Total** | **12,851** | **100%** |

## 2. Emotion Label Distribution

### Train Set
| Emotion | Sentences | Percentage |
|---------|-----------|------------|
| Anger | 1,186 | 10.34% |
| Disgust | 1,771 | 15.44% |
| Enjoyment | 3,246 | 28.29% |
| Fear | 559 | 4.87% |
| Other | 2,204 | 19.21% |
| Sadness | 1,990 | 17.35% |
| Surprise | 515 | 4.49% |
| **Total** | **11,472** | **100%** |

**Class Imbalance Ratio**: 6.30 (Most frequent / Least frequent)

### Validation Set
| Emotion | Sentences | Percentage |
|---------|-----------|------------|
| Anger | 49 | 7.14% |
| Disgust | 135 | 19.68% |
| Enjoyment | 214 | 31.20% |
| Fear | 31 | 4.52% |
| Other | 141 | 20.55% |
| Sadness | 86 | 12.54% |
| Surprise | 30 | 4.37% |

### Test Set
| Emotion | Sentences | Percentage |
|---------|-----------|------------|
| Anger | 40 | 5.77% |
| Disgust | 132 | 19.05% |
| Enjoyment | 193 | 27.85% |
| Fear | 46 | 6.64% |
| Other | 129 | 18.61% |
| Sadness | 116 | 16.74% |
| Surprise | 37 | 5.34% |

## 3. Sentence Length Statistics

### 3.1 Basic Statistics

| Metric | Train | Val | Test |
|--------|-------|-----|------|
| Mean | 12.83 | 14.18 | 13.81 |
| Std Dev | 8.31 | 9.47 | 9.08 |
| Min | 1 | 2 | 2 |
| Max | 164 | 80 | 64 |
| Median | 11.0 | 12.0 | 11.0 |

### 3.2 Length Distribution by Emotion (Train Set)

Distribution of sentence lengths across different emotions (percentage of total dataset):

| Length | Anger | Disgust | Enjoyment | Fear | Other | Sadness | Surprise | Overall | 
|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 1-5 | 0.92 | 1.82 | 4.52 | 0.65 | 1.63 | 1.63 | 0.64 | 11.80 | 
| 6-10 | 3.05 | 4.34 | 11.05 | 1.67 | 7.59 | 5.79 | 2.12 | 35.61 | 
| 10-15 | 2.51 | 3.48 | 6.22 | 1.17 | 4.91 | 4.59 | 1.14 | 24.02 | 
| 16-20 | 2.35 | 2.89 | 4.08 | 0.77 | 3.57 | 3.14 | 0.47 | 17.26 | 
| 21-25 | 0.65 | 1.21 | 1.26 | 0.19 | 0.99 | 1.24 | 0.12 | 5.65 | 
| 26-30 | 0.29 | 0.68 | 0.60 | 0.17 | 0.35 | 0.57 | 0.00 | 2.65 | 
| >30 | 0.58 | 1.02 | 0.58 | 0.25 | 0.17 | 0.39 | 0.00 | 3.01 | 
| **Total** | **10.34** | **15.44** | **28.30** | **4.87** | **19.21** | **17.35** | **4.49** | **100.00** | 

**Observations**:
- Most sentences fall in the 6-10 and 10-15 word ranges
- Very short (1-5) and very long (>30) sentences are less common
- Emotion distribution varies across length ranges

## 4. Vocabulary Statistics (Train set)

| Metric | Value |
|--------|-------|
| Total words (tokens) | 147,153 |
| Unique words (vocab) | 9,346 |
| Vocab richness | 6.35% |

## 5. Data Quality Notes

- **Source**: UIT-VSMEC (train/val/test) + Self-collected comments (merged into train)
- **Language**: Vietnamese (social media text)
- **Preprocessing status**: Raw data (before normalization and word segmentation)
- **Class distribution**: Imbalanced - Enjoyment is most frequent, Surprise is least frequent
