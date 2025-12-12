"""
Script để chuẩn bị dữ liệu cho Google Colab
Tạo file zip chứa dữ liệu đã tiền xử lý
"""
import zipfile
import os
from pathlib import Path

def create_data_zip():
    """Tạo file zip chứa dữ liệu processed"""
    
    # Các file cần nén
    files_to_zip = [
        'data/processed/train.csv',
        'data/processed/val.csv',
        'data/processed/test.csv',
    ]
    
    # Tên file zip
    zip_path = 'processed_data.zip'
    
    print("=" * 60)
    print("CHUẨN BỊ DỮ LIỆU CHO GOOGLE COLAB")
    print("=" * 60)
    
    # Kiểm tra file tồn tại
    missing_files = []
    for file in files_to_zip:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("\n❌ THIẾU CÁC FILE SAU:")
        for f in missing_files:
            print(f"  - {f}")
        print("\nVui lòng chạy tiền xử lý trước!")
        return
    
    # Tạo file zip
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_zip:
            print(f"✓ Đang nén: {file}")
            zipf.write(file, arcname=os.path.basename(file))
    
    # Thống kê
    zip_size = os.path.getsize(zip_path) / (1024 * 1024)  # MB
    
    print("\n" + "=" * 60)
    print("✅ HOÀN THÀNH!")
    print("=" * 60)
    print(f"File zip: {zip_path}")
    print(f"Kích thước: {zip_size:.2f} MB")
    print("\nCác file trong zip:")
    for file in files_to_zip:
        print(f"  - {os.path.basename(file)}")
    
    print("\n" + "=" * 60)
    print("BƯỚC TIẾP THEO:")
    print("=" * 60)
    print("1. Upload file 'processed_data.zip' lên Google Drive")
    print("2. Mở Google Colab: https://colab.research.google.com")
    print("3. Làm theo hướng dẫn trong file: colab_training_guide.md")

if __name__ == "__main__":
    create_data_zip()



