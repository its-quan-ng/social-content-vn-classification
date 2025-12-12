"""
Setup VnCoreNLP
===============
Download và cài đặt VnCoreNLP models.
"""

import os
from pathlib import Path

try:
    import py_vncorenlp
    print("✓ py_vncorenlp đã được cài đặt")
except ImportError:
    print("❌ Chưa cài py_vncorenlp. Chạy: pip install py_vncorenlp")
    exit(1)

# Tạo thư mục lưu models
project_root = Path(__file__).parent.parent
vncorenlp_dir = project_root / "vncorenlp"
vncorenlp_dir.mkdir(exist_ok=True)

print("\n" + "=" * 80)
print("DOWNLOADING VNCORENLP MODELS")
print("=" * 80)
print(f"\nDownload path: {vncorenlp_dir}")
print("File size: ~130 MB")
print("Đợi một chút nhé...\n")

try:
    # Download models
    py_vncorenlp.download_model(save_dir=str(vncorenlp_dir))
    
    print("\n" + "=" * 80)
    print("✅ DOWNLOAD THÀNH CÔNG!")
    print("=" * 80)
    
    # List downloaded files
    print(f"\nFiles trong {vncorenlp_dir}:")
    for file in vncorenlp_dir.rglob("*"):
        if file.is_file():
            size_mb = file.stat().st_size / (1024 * 1024)
            print(f"  - {file.name} ({size_mb:.1f} MB)")
    
    # Test
    print("\n" + "=" * 80)
    print("TESTING VNCORENLP")
    print("=" * 80)
    
    # Find the jar file
    jar_files = list(vncorenlp_dir.rglob("*.jar"))
    if jar_files:
        jar_path = jar_files[0]
        print(f"\n✓ Found JAR file: {jar_path}")
        print(f"\n📝 Để sử dụng VnCoreNLP, dùng đường dẫn:")
        print(f"   {jar_path}")
        
        # Save to config file
        config_file = project_root / "vncorenlp_config.txt"
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(f"VNCORENLP_PATH={jar_path}\n")
        
        print(f"\n✓ Đã lưu config vào: {config_file}")
        
        # Test segmentation
        print("\n" + "-" * 80)
        print("Test word segmentation:")
        print("-" * 80)
        
        try:
            from vncorenlp import VnCoreNLP
            
            rdrsegmenter = VnCoreNLP(str(jar_path), annotators="wseg", max_heap_size='-Xmx2g')
            
            test_text = "Sản phẩm này chất lượng tốt"
            result = rdrsegmenter.tokenize(test_text)
            
            print(f"\nInput:  {test_text}")
            print(f"Output: {' '.join(result[0])}")
            
            rdrsegmenter.close()
            
            print("\n✅ VnCoreNLP hoạt động tốt!")
            
        except Exception as e:
            print(f"\n⚠️  Không thể test VnCoreNLP: {e}")
            print("    Nhưng file đã được download, bạn có thể dùng được!")
    
    else:
        print("\n⚠️  Không tìm thấy JAR file")
        print("    Vui lòng download thủ công từ:")
        print("    https://github.com/vncorenlp/VnCoreNLP/releases")
    
except Exception as e:
    print(f"\n❌ LỖI: {e}")
    print("\n" + "=" * 80)
    print("HƯỚNG DẪN CÀI THỦ CÔNG")
    print("=" * 80)
    print("""
1. Download VnCoreNLP từ:
   https://github.com/vncorenlp/VnCoreNLP/releases
   
2. Giải nén file .zip
   
3. Chạy lại preprocessing với option:
   python scripts/preprocess_data.py \\
       --input-dir data/raw \\
       --output-dir data/processed \\
       --vncorenlp-path "D:/path/to/VnCoreNLP-1.1.1.jar"
""")

