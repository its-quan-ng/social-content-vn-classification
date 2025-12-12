# 🚀 Quick Start: Fine-tune PhoBERT trên Google Colab

## 📌 TÓM TẮT 3 BƯỚC

### 1️⃣ Chuẩn bị dữ liệu (Máy local)

```bash
# Tạo file zip
python scripts/prepare_for_colab.py
```

👉 File `processed_data.zip` (0.59 MB) sẽ được tạo ở thư mục gốc

### 2️⃣ Upload lên Google Drive

1. Mở https://drive.google.com
2. Tạo thư mục (ví dụ: `PPNCKH`)
3. Upload file `processed_data.zip`

### 3️⃣ Chạy training trên Colab

1. Mở https://colab.research.google.com
2. Tạo notebook mới
3. Bật GPU: **Runtime** → **Change runtime type** → **GPU (T4)**
4. Copy-paste code từ file `colab_training_guide.md` (17 cells)

---

## ⏱️ THỜI GIAN DỰ KIẾN

- **Chuẩn bị**: 2 phút
- **Training**: 25-50 phút (5 epochs × 5-10 phút/epoch)
- **Tổng**: ~30-60 phút

---

## 📊 KẾT QUẢ MONG ĐỢI

Sau khi training, bạn sẽ có:

- ✅ `best_model.pt` - Model fine-tuned
- ✅ `training_history.png` - Biểu đồ loss/accuracy/F1
- ✅ `confusion_matrix.png` - Ma trận nhầm lẫn
- ✅ `test_results.json` - Accuracy & F1-score

**Kết quả dự kiến trên test set:**
- Accuracy: ~70-80%
- F1-score (weighted): ~68-78%

---

## 📖 CHI TIẾT

Xem hướng dẫn đầy đủ trong file: **`colab_training_guide.md`**

---

## ❓ TROUBLESHOOTING

| Lỗi | Giải pháp |
|-----|-----------|
| "File not found" | Kiểm tra đường dẫn zip trong cell 4 |
| "CUDA out of memory" | Giảm BATCH_SIZE xuống 8 hoặc 4 |
| "Runtime disconnected" | Reconnect và chạy lại từ cell mount Drive |

---

## 🎯 BƯỚC TIẾP THEO SAU TRAINING

1. **Phân tích kết quả**: Xem confusion matrix, tìm lớp nào bị nhầm nhiều
2. **So sánh baseline**: So với các phương pháp khác (SVM, LSTM, etc.)
3. **Viết báo cáo**: Tóm tắt kết quả trong phần "3.5. Kết quả thực nghiệm"
4. **Thử nghiệm thêm**: 
   - Tăng epochs (thử 10-15 epochs)
   - Điều chỉnh learning rate (thử 1e-5, 3e-5, 5e-5)
   - Thử PhoBERT-large (thay vì base)
   - Thử thêm layers (BiLSTM trên PhoBERT output)

---

Good luck! 🎉



