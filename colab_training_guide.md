# 🚀 Hướng dẫn Fine-tune PhoBERT trên Google Colab

## 📋 BƯỚC 1: CHUẨN BỊ DỮ LIỆU

### 1.1. Tạo file zip

Chạy lệnh sau để tạo file `processed_data.zip`:

```bash
python scripts/prepare_for_colab.py
```

File zip sẽ được tạo ở thư mục gốc project, chứa 3 file:
- `train.csv`
- `val.csv`
- `test.csv`

### 1.2. Upload lên Google Drive

1. Mở Google Drive: https://drive.google.com
2. Tạo thư mục mới (ví dụ: `PPNCKH`)
3. Upload file `processed_data.zip` vào thư mục đó

---

## 🎯 BƯỚC 2: MỞ GOOGLE COLAB

### 2.1. Tạo Notebook mới

1. Truy cập: https://colab.research.google.com
2. Click **New Notebook**
3. Đổi tên notebook: `PhoBERT_Emotion_Classification`

### 2.2. Bật GPU

1. Click **Runtime** → **Change runtime type**
2. Chọn **Hardware accelerator**: **GPU** (T4)
3. Click **Save**

---

## 💻 BƯỚC 3: CODE TRONG COLAB

Copy từng cell code dưới đây vào Colab và chạy tuần tự:

### Cell 1: Kiểm tra GPU

```python
!nvidia-smi
```

### Cell 2: Cài đặt thư viện

```python
!pip install -q transformers torch torchvision torchaudio
!pip install -q scikit-learn pandas numpy matplotlib seaborn
```

### Cell 3: Mount Google Drive

```python
from google.colab import drive
drive.mount('/content/drive')
```

> **Lưu ý:** Bạn sẽ được yêu cầu đăng nhập Google và cho phép truy cập Drive.

### Cell 4: Giải nén dữ liệu

```python
import zipfile
import os

# Thay đổi đường dẫn này theo vị trí file zip của bạn
zip_path = '/content/drive/MyDrive/PPNCKH/processed_data.zip'

# Giải nén
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall('/content/data')

print("✅ Giải nén hoàn tất!")
print("\nCác file:")
!ls -lh /content/data/
```

### Cell 5: Load và khám phá dữ liệu

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
train_df = pd.read_csv('/content/data/train.csv')
val_df = pd.read_csv('/content/data/val.csv')
test_df = pd.read_csv('/content/data/test.csv')

print("="*60)
print("THỐNG KÊ DỮ LIỆU")
print("="*60)
print(f"Train: {len(train_df):,} câu")
print(f"Val:   {len(val_df):,} câu")
print(f"Test:  {len(test_df):,} câu")
print(f"Total: {len(train_df) + len(val_df) + len(test_df):,} câu")

print("\n" + "="*60)
print("PHÂN PHỐI CÁC LỚP CẢM XÚC (TRAIN SET)")
print("="*60)
print(train_df['Emotion'].value_counts())

# Vẽ biểu đồ
plt.figure(figsize=(10, 6))
train_df['Emotion'].value_counts().plot(kind='bar', color='skyblue')
plt.title('Phân phối cảm xúc trong tập Train', fontsize=14, weight='bold')
plt.xlabel('Cảm xúc')
plt.ylabel('Số lượng câu')
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# Hiển thị 5 mẫu
print("\n5 mẫu dữ liệu:")
display(train_df[['Emotion', 'Sentence_processed']].head())
```

### Cell 6: Load PhoBERT và Tokenizer

```python
from transformers import AutoModel, AutoTokenizer

# Load PhoBERT-base
MODEL_NAME = "vinai/phobert-base"

print(f"Đang load model: {MODEL_NAME}...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
phobert = AutoModel.from_pretrained(MODEL_NAME)

print("✅ Load model thành công!")
print(f"\nVocab size: {tokenizer.vocab_size:,}")
print(f"Model parameters: {phobert.num_parameters():,}")

# Test tokenizer
sample_text = train_df.iloc[0]['Sentence_processed']
print(f"\nText gốc:\n{sample_text}")
print(f"\nTokens:\n{tokenizer.tokenize(sample_text)}")
```

### Cell 7: Phân tích độ dài token

```python
# Tính độ dài token
train_df['token_length'] = train_df['Sentence_processed'].apply(
    lambda x: len(tokenizer.encode(x, add_special_tokens=True))
)

print("="*60)
print("THỐNG KÊ ĐỘ DÀI TOKEN")
print("="*60)
print(f"Mean:   {train_df['token_length'].mean():.2f}")
print(f"Median: {train_df['token_length'].median():.0f}")
print(f"Min:    {train_df['token_length'].min()}")
print(f"Max:    {train_df['token_length'].max()}")
print(f"95th percentile: {train_df['token_length'].quantile(0.95):.0f}")

# Vẽ histogram
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.hist(train_df['token_length'], bins=50, color='skyblue', edgecolor='black')
plt.axvline(train_df['token_length'].mean(), color='red', linestyle='--', 
            label=f'Mean: {train_df["token_length"].mean():.1f}')
plt.axvline(train_df['token_length'].quantile(0.95), color='green', linestyle='--', 
            label=f'95th: {train_df["token_length"].quantile(0.95):.0f}')
plt.xlabel('Số lượng tokens')
plt.ylabel('Tần suất')
plt.title('Phân phối độ dài token')
plt.legend()
plt.grid(alpha=0.3)

plt.subplot(1, 2, 2)
plt.boxplot(train_df['token_length'])
plt.ylabel('Số lượng tokens')
plt.title('Boxplot độ dài token')
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()

# Đề xuất max_length
recommended_max_length = int(train_df['token_length'].quantile(0.95))
print(f"\n💡 Đề xuất max_length: {recommended_max_length}")
```

### Cell 8: Định nghĩa Dataset class

```python
import torch
from torch.utils.data import Dataset, DataLoader

class EmotionDataset(Dataset):
    def __init__(self, dataframe, tokenizer, max_length=128):
        self.data = dataframe.reset_index(drop=True)
        self.tokenizer = tokenizer
        self.max_length = max_length
        
        # Map emotion labels to integers
        self.label_map = {
            'Enjoyment': 0,
            'Sadness': 1,
            'Anger': 2,
            'Fear': 3,
            'Disgust': 4,
            'Surprise': 5,
            'Other': 6
        }
        self.reverse_label_map = {v: k for k, v in self.label_map.items()}
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        text = str(self.data.loc[idx, 'Sentence_processed'])
        emotion = self.data.loc[idx, 'Emotion']
        label = self.label_map[emotion]
        
        # Tokenize
        encoding = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(label, dtype=torch.long)
        }

print("✅ EmotionDataset class đã được định nghĩa!")
```

### Cell 9: Tạo DataLoaders

```python
# Hyperparameters
MAX_LENGTH = 128  # Có thể điều chỉnh dựa trên phân tích
BATCH_SIZE = 16

# Tạo datasets
train_dataset = EmotionDataset(train_df, tokenizer, max_length=MAX_LENGTH)
val_dataset = EmotionDataset(val_df, tokenizer, max_length=MAX_LENGTH)
test_dataset = EmotionDataset(test_df, tokenizer, max_length=MAX_LENGTH)

# Tạo dataloaders
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

print("="*60)
print("DATALOADERS")
print("="*60)
print(f"Train batches: {len(train_loader)}")
print(f"Val batches:   {len(val_loader)}")
print(f"Test batches:  {len(test_loader)}")
print(f"\nBatch size: {BATCH_SIZE}")
print(f"Max length: {MAX_LENGTH}")

# Test dataloader
batch = next(iter(train_loader))
print("\n" + "="*60)
print("TEST BATCH")
print("="*60)
print(f"Input IDs shape: {batch['input_ids'].shape}")
print(f"Attention mask shape: {batch['attention_mask'].shape}")
print(f"Labels shape: {batch['label'].shape}")
```

### Cell 10: Định nghĩa Model

```python
import torch.nn as nn

class PhoBERTEmotionClassifier(nn.Module):
    def __init__(self, num_classes=7, dropout=0.3):
        super(PhoBERTEmotionClassifier, self).__init__()
        
        # Load PhoBERT
        self.phobert = AutoModel.from_pretrained(MODEL_NAME)
        
        # Classification head
        self.dropout = nn.Dropout(dropout)
        self.classifier = nn.Linear(self.phobert.config.hidden_size, num_classes)
    
    def forward(self, input_ids, attention_mask):
        # PhoBERT outputs
        outputs = self.phobert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        
        # Use [CLS] token representation (first token)
        pooled_output = outputs.last_hidden_state[:, 0, :]
        
        # Classification
        pooled_output = self.dropout(pooled_output)
        logits = self.classifier(pooled_output)
        
        return logits

# Khởi tạo model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = PhoBERTEmotionClassifier(num_classes=7, dropout=0.3)
model = model.to(device)

print("="*60)
print("MODEL INITIALIZED")
print("="*60)
print(f"Device: {device}")
print(f"Total parameters: {sum(p.numel() for p in model.parameters()):,}")
print(f"Trainable parameters: {sum(p.numel() for p in model.parameters() if p.requires_grad):,}")
```

### Cell 11: Training Setup

```python
from torch.optim import AdamW
from transformers import get_linear_schedule_with_warmup

# Hyperparameters
EPOCHS = 5
LEARNING_RATE = 2e-5
WARMUP_STEPS = 0
WEIGHT_DECAY = 0.01

# Optimizer
optimizer = AdamW(
    model.parameters(),
    lr=LEARNING_RATE,
    weight_decay=WEIGHT_DECAY
)

# Learning rate scheduler
total_steps = len(train_loader) * EPOCHS
scheduler = get_linear_schedule_with_warmup(
    optimizer,
    num_warmup_steps=WARMUP_STEPS,
    num_training_steps=total_steps
)

# Loss function
criterion = nn.CrossEntropyLoss()

print("="*60)
print("TRAINING SETUP")
print("="*60)
print(f"Epochs: {EPOCHS}")
print(f"Learning rate: {LEARNING_RATE}")
print(f"Batch size: {BATCH_SIZE}")
print(f"Total training steps: {total_steps}")
```

### Cell 12: Định nghĩa Training Functions

```python
from tqdm.notebook import tqdm
from sklearn.metrics import accuracy_score, f1_score

def train_epoch(model, data_loader, optimizer, scheduler, criterion, device):
    model.train()
    total_loss = 0
    predictions = []
    true_labels = []
    
    progress_bar = tqdm(data_loader, desc='Training')
    
    for batch in progress_bar:
        # Move batch to device
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['label'].to(device)
        
        # Forward pass
        optimizer.zero_grad()
        logits = model(input_ids, attention_mask)
        loss = criterion(logits, labels)
        
        # Backward pass
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        scheduler.step()
        
        # Track metrics
        total_loss += loss.item()
        preds = torch.argmax(logits, dim=1).cpu().numpy()
        predictions.extend(preds)
        true_labels.extend(labels.cpu().numpy())
        
        progress_bar.set_postfix({'loss': loss.item()})
    
    avg_loss = total_loss / len(data_loader)
    accuracy = accuracy_score(true_labels, predictions)
    f1 = f1_score(true_labels, predictions, average='weighted')
    
    return avg_loss, accuracy, f1

def eval_epoch(model, data_loader, criterion, device):
    model.eval()
    total_loss = 0
    predictions = []
    true_labels = []
    
    progress_bar = tqdm(data_loader, desc='Evaluating')
    
    with torch.no_grad():
        for batch in progress_bar:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['label'].to(device)
            
            logits = model(input_ids, attention_mask)
            loss = criterion(logits, labels)
            
            total_loss += loss.item()
            preds = torch.argmax(logits, dim=1).cpu().numpy()
            predictions.extend(preds)
            true_labels.extend(labels.cpu().numpy())
    
    avg_loss = total_loss / len(data_loader)
    accuracy = accuracy_score(true_labels, predictions)
    f1 = f1_score(true_labels, predictions, average='weighted')
    
    return avg_loss, accuracy, f1, predictions, true_labels

print("✅ Training functions đã được định nghĩa!")
```

### Cell 13: BẮT ĐẦU TRAINING 🚀

```python
# Training history
history = {
    'train_loss': [],
    'train_acc': [],
    'train_f1': [],
    'val_loss': [],
    'val_acc': [],
    'val_f1': []
}

best_val_f1 = 0

print("="*60)
print("BẮT ĐẦU TRAINING")
print("="*60)

for epoch in range(EPOCHS):
    print(f"\n{'='*60}")
    print(f"Epoch {epoch + 1}/{EPOCHS}")
    print(f"{'='*60}")
    
    # Train
    train_loss, train_acc, train_f1 = train_epoch(
        model, train_loader, optimizer, scheduler, criterion, device
    )
    
    # Evaluate
    val_loss, val_acc, val_f1, _, _ = eval_epoch(
        model, val_loader, criterion, device
    )
    
    # Save history
    history['train_loss'].append(train_loss)
    history['train_acc'].append(train_acc)
    history['train_f1'].append(train_f1)
    history['val_loss'].append(val_loss)
    history['val_acc'].append(val_acc)
    history['val_f1'].append(val_f1)
    
    # Print metrics
    print(f"\nTrain Loss: {train_loss:.4f} | Train Acc: {train_acc:.4f} | Train F1: {train_f1:.4f}")
    print(f"Val Loss:   {val_loss:.4f} | Val Acc:   {val_acc:.4f} | Val F1:   {val_f1:.4f}")
    
    # Save best model
    if val_f1 > best_val_f1:
        best_val_f1 = val_f1
        torch.save(model.state_dict(), '/content/best_model.pt')
        print(f"✅ Saved best model! (Val F1: {val_f1:.4f})")

print("\n" + "="*60)
print("✅ TRAINING HOÀN TẤT!")
print("="*60)
print(f"Best Val F1: {best_val_f1:.4f}")
```

### Cell 14: Visualize Training History

```python
# Plot training history
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Loss
axes[0].plot(history['train_loss'], label='Train Loss', marker='o')
axes[0].plot(history['val_loss'], label='Val Loss', marker='o')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Loss')
axes[0].set_title('Loss Over Epochs')
axes[0].legend()
axes[0].grid(alpha=0.3)

# Accuracy
axes[1].plot(history['train_acc'], label='Train Acc', marker='o')
axes[1].plot(history['val_acc'], label='Val Acc', marker='o')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Accuracy')
axes[1].set_title('Accuracy Over Epochs')
axes[1].legend()
axes[1].grid(alpha=0.3)

# F1 Score
axes[2].plot(history['train_f1'], label='Train F1', marker='o')
axes[2].plot(history['val_f1'], label='Val F1', marker='o')
axes[2].set_xlabel('Epoch')
axes[2].set_ylabel('F1 Score')
axes[2].set_title('F1 Score Over Epochs')
axes[2].legend()
axes[2].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('/content/training_history.png', dpi=300, bbox_inches='tight')
plt.show()
```

### Cell 15: Đánh giá trên Test Set

```python
from sklearn.metrics import classification_report, confusion_matrix

# Load best model
model.load_state_dict(torch.load('/content/best_model.pt'))

# Evaluate on test set
test_loss, test_acc, test_f1, test_predictions, test_true_labels = eval_epoch(
    model, test_loader, criterion, device
)

print("="*60)
print("KẾT QUẢ TRÊN TEST SET")
print("="*60)
print(f"Test Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_acc:.4f}")
print(f"Test F1 Score: {test_f1:.4f}")

# Classification report
label_names = ['Enjoyment', 'Sadness', 'Anger', 'Fear', 'Disgust', 'Surprise', 'Other']

print("\n" + "="*60)
print("CLASSIFICATION REPORT")
print("="*60)
print(classification_report(test_true_labels, test_predictions, 
                          target_names=label_names, digits=4))
```

### Cell 16: Confusion Matrix

```python
# Confusion matrix
cm = confusion_matrix(test_true_labels, test_predictions)

plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=label_names, yticklabels=label_names)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix - Test Set')
plt.tight_layout()
plt.savefig('/content/confusion_matrix.png', dpi=300, bbox_inches='tight')
plt.show()
```

### Cell 17: Lưu kết quả về Google Drive

```python
import shutil
import json

# Tạo thư mục lưu kết quả
output_dir = '/content/drive/MyDrive/phobert_emotion_results'
!mkdir -p {output_dir}

# Copy model
shutil.copy('/content/best_model.pt', f'{output_dir}/best_model.pt')

# Copy figures
shutil.copy('/content/training_history.png', f'{output_dir}/training_history.png')
shutil.copy('/content/confusion_matrix.png', f'{output_dir}/confusion_matrix.png')

# Save history
with open(f'{output_dir}/training_history.json', 'w') as f:
    json.dump(history, f, indent=2)

# Save test results
test_results = {
    'test_loss': test_loss,
    'test_accuracy': test_acc,
    'test_f1': test_f1
}
with open(f'{output_dir}/test_results.json', 'w') as f:
    json.dump(test_results, f, indent=2)

print("="*60)
print("✅ ĐÃ LƯU KẾT QUẢ VỀ GOOGLE DRIVE")
print("="*60)
print(f"Thư mục: {output_dir}")
print("\nCác file:")
!ls -lh {output_dir}
```

---

## 🎉 HOÀN TẤT!

Bạn đã fine-tune thành công PhoBERT cho bài toán phân loại cảm xúc tiếng Việt!

**Kết quả đã lưu:**
- `best_model.pt` - Model có kết quả tốt nhất
- `training_history.png` - Biểu đồ quá trình training
- `confusion_matrix.png` - Ma trận nhầm lẫn
- `training_history.json` - Lịch sử training
- `test_results.json` - Kết quả trên test set

---

## 📝 LƯU Ý

1. **Thời gian training**: Với GPU T4 trên Colab, mỗi epoch mất khoảng 5-10 phút
2. **Session timeout**: Colab free có giới hạn thời gian, hãy đảm bảo lưu kết quả về Drive
3. **Điều chỉnh hyperparameters**: Bạn có thể thay đổi `EPOCHS`, `BATCH_SIZE`, `LEARNING_RATE`, `MAX_LENGTH` để tối ưu kết quả
4. **GPU memory**: Nếu gặp lỗi OOM (Out of Memory), giảm `BATCH_SIZE` hoặc `MAX_LENGTH`

---

## 🔧 TROUBLESHOOTING

**Lỗi: "Runtime disconnected"**
- Giải pháp: Reconnect và chạy lại từ cell mount Drive

**Lỗi: "CUDA out of memory"**
- Giải pháp: Giảm BATCH_SIZE xuống 8 hoặc 4

**Lỗi: "File not found"**
- Giải pháp: Kiểm tra lại đường dẫn file zip trong cell 4

