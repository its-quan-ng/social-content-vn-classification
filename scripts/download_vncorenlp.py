"""
Download VnCoreNLP
==================
Download VnCoreNLP JAR file trực tiếp.
"""

import urllib.request
import zipfile
from pathlib import Path
from tqdm import tqdm

project_root = Path(__file__).parent.parent
vncorenlp_dir = project_root / "vncorenlp"
vncorenlp_dir.mkdir(exist_ok=True)

print("=" * 80)
print("DOWNLOADING VNCORENLP")
print("=" * 80)

# URL download
url = "https://github.com/vncorenlp/VnCoreNLP/archive/refs/heads/master.zip"
zip_file = vncorenlp_dir / "VnCoreNLP.zip"

print(f"\nDownloading from: {url}")
print(f"Save to: {zip_file}")
print("\nĐợi một chút, file ~130 MB...")

try:
    # Download với progress bar
    class DownloadProgressBar(tqdm):
        def update_to(self, b=1, bsize=1, tsize=None):
            if tsize is not None:
                self.total = tsize
            self.update(b * bsize - self.n)
    
    with DownloadProgressBar(unit='B', unit_scale=True, miniters=1) as t:
        urllib.request.urlretrieve(url, zip_file, reporthook=t.update_to)
    
    print(f"\n✓ Download thành công!")
    
    # Extract
    print(f"\nĐang giải nén...")
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(vncorenlp_dir)
    
    print(f"✓ Giải nén xong!")
    
    # Find JAR files
    jar_files = list(vncorenlp_dir.rglob("*.jar"))
    
    if jar_files:
        print(f"\n✅ Tìm thấy {len(jar_files)} JAR files:")
        for jar in jar_files:
            size_mb = jar.stat().st_size / (1024 * 1024)
            print(f"   - {jar.name} ({size_mb:.1f} MB)")
            print(f"     Path: {jar}")
        
        # Lưu config
        main_jar = jar_files[0]
        config_file = project_root / "vncorenlp_config.txt"
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(f"{main_jar}\n")
        
        print(f"\n✓ Đã lưu config vào: {config_file}")
        print("\n" + "=" * 80)
        print("CÁCH SỬ DỤNG")
        print("=" * 80)
        print(f"""
Để dùng VnCoreNLP trong preprocessing, chạy:

python scripts/preprocess_data.py \\
    --input-dir data/raw \\
    --output-dir data/processed \\
    --vncorenlp-path "{main_jar}"

Hoặc trong code Python:

from src.preprocessing import PreprocessingPipeline

pipeline = PreprocessingPipeline(
    vncorenlp_path=r"{main_jar}",
    segmentation_method='vncorenlp'
)
""")
    else:
        print("\n⚠️  Không tìm thấy JAR file sau khi giải nén")
        print("    Bạn cần download thủ công từ:")
        print("    https://github.com/vncorenlp/VnCoreNLP/releases")
    
    # Cleanup zip
    zip_file.unlink()
    print(f"\n✓ Đã xóa file zip")
    
except Exception as e:
    print(f"\n❌ LỖI: {e}")
    print("\n" + "=" * 80)
    print("DOWNLOAD THỦ CÔNG")
    print("=" * 80)
    print("""
Nếu script không hoạt động, hãy download thủ công:

1. Vào: https://github.com/vncorenlp/VnCoreNLP/releases
2. Download file: VnCoreNLP-1.1.1.jar (~130 MB)
3. Lưu vào thư mục vncorenlp/
4. Dùng đường dẫn đó khi chạy preprocessing
""")

