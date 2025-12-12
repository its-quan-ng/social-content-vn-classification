"""
Preprocess Data Script
======================
Tiền xử lý toàn bộ dữ liệu train/val/test cho PhoBERT fine-tuning.

Usage:
    python scripts/preprocess_data.py --input data/raw/train_merged.csv --output data/processed/train.csv

Author: PPNCKH Project
"""

import sys
import argparse
from pathlib import Path
import pandas as pd
from datetime import datetime

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.preprocessing import PreprocessingPipeline


def preprocess_file(input_file: Path, 
                    output_file: Path,
                    text_column: str = 'Sentence',
                    label_column: str = 'Emotion',
                    slang_dict_path: Path = None,
                    word_segmentation: bool = True,
                    min_word_count: int = 3,
                    save_stats: bool = True,
                    vncorenlp_path: Path = None,
                    segmentation_method: str = 'pyvi'):
    """
    Tiền xử lý một file dữ liệu
    
    Args:
        input_file: File CSV/Excel đầu vào
        output_file: File CSV đầu ra
        text_column: Tên cột chứa văn bản
        label_column: Tên cột chứa nhãn
        slang_dict_path: Đường dẫn đến từ điển slang
        word_segmentation: Có tách từ không
        min_word_count: Số từ tối thiểu
        save_stats: Lưu file statistics
        vncorenlp_path: Đường dẫn đến VnCoreNLP JAR file
        segmentation_method: Phương pháp tách từ ('pyvi' hoặc 'vncorenlp')
    """
    print("=" * 80)
    print(f"PREPROCESSING: {input_file.name}")
    print("=" * 80)
    
    # Đọc file
    print(f"\n📂 Loading data from {input_file}...")
    
    if input_file.suffix == '.csv':
        df = pd.read_csv(input_file, encoding='utf-8-sig')
    elif input_file.suffix in ['.xlsx', '.xls']:
        df = pd.read_excel(input_file)
    else:
        raise ValueError(f"Unsupported file format: {input_file.suffix}")
    
    print(f"   Loaded {len(df)} rows")
    
    # Kiểm tra columns
    if text_column not in df.columns:
        raise ValueError(f"Column '{text_column}' not found in {input_file}")
    
    # Show original stats
    print(f"\n📊 Original Data:")
    print(f"   Total rows: {len(df)}")
    if label_column in df.columns:
        print(f"   Label distribution:")
        for label, count in df[label_column].value_counts().items():
            print(f"      {label}: {count} ({count/len(df)*100:.1f}%)")
    
    # Khởi tạo pipeline
    print(f"\n⚙️  Initializing preprocessing pipeline...")
    
    # Auto-detect segmentation method từ vncorenlp_path
    if vncorenlp_path is not None:
        segmentation_method = 'vncorenlp'
    
    pipeline = PreprocessingPipeline(
        slang_dict_path=slang_dict_path,
        word_segmentation=word_segmentation,
        segmentation_method=segmentation_method,
        vncorenlp_path=vncorenlp_path,
        min_word_count=min_word_count,
        lowercase=True
    )
    
    print(f"   Pipeline config:")
    for key, value in pipeline.get_pipeline_info().items():
        print(f"      {key}: {value}")
    
    # Tiền xử lý
    print(f"\n🔄 Processing...")
    df_processed = pipeline.preprocess_dataframe(
        df,
        text_column=text_column,
        output_column='Sentence_processed',
        keep_original=True,
        filter_invalid=True
    )
    
    # Show processed stats
    print(f"\n📊 Processed Data:")
    print(f"   Total rows: {len(df_processed)}")
    print(f"   Filtered: {len(df) - len(df_processed)} rows ({(len(df) - len(df_processed))/len(df)*100:.1f}%)")
    
    if label_column in df_processed.columns:
        print(f"   Label distribution:")
        for label, count in df_processed[label_column].value_counts().items():
            print(f"      {label}: {count} ({count/len(df_processed)*100:.1f}%)")
    
    print(f"\n   Word count statistics:")
    print(f"      Mean: {df_processed['word_count'].mean():.1f}")
    print(f"      Median: {df_processed['word_count'].median():.0f}")
    print(f"      Min: {df_processed['word_count'].min()}")
    print(f"      Max: {df_processed['word_count'].max()}")
    
    # Lưu file
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df_processed.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n✅ Saved to: {output_file}")
    
    # Lưu statistics
    if save_stats:
        stats_file = output_file.parent / f"{output_file.stem}_stats.txt"
        with open(stats_file, 'w', encoding='utf-8') as f:
            f.write(f"Preprocessing Statistics\n")
            f.write(f"{'=' * 60}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Input file: {input_file}\n")
            f.write(f"Output file: {output_file}\n\n")
            
            f.write(f"Original data:\n")
            f.write(f"  Total rows: {len(df)}\n")
            
            f.write(f"\nProcessed data:\n")
            f.write(f"  Total rows: {len(df_processed)}\n")
            f.write(f"  Filtered: {len(df) - len(df_processed)} rows\n")
            f.write(f"  Retention rate: {len(df_processed)/len(df)*100:.2f}%\n")
            
            if label_column in df_processed.columns:
                f.write(f"\nLabel distribution:\n")
                for label, count in df_processed[label_column].value_counts().items():
                    f.write(f"  {label}: {count} ({count/len(df_processed)*100:.1f}%)\n")
            
            f.write(f"\nWord count statistics:\n")
            f.write(f"  Mean: {df_processed['word_count'].mean():.2f}\n")
            f.write(f"  Median: {df_processed['word_count'].median():.0f}\n")
            f.write(f"  Std: {df_processed['word_count'].std():.2f}\n")
            f.write(f"  Min: {df_processed['word_count'].min()}\n")
            f.write(f"  Max: {df_processed['word_count'].max()}\n")
            
            f.write(f"\nPipeline configuration:\n")
            for key, value in pipeline.get_pipeline_info().items():
                f.write(f"  {key}: {value}\n")
        
        print(f"📊 Statistics saved to: {stats_file}")
    
    return df_processed


def preprocess_all_splits(data_dir: Path,
                          output_dir: Path,
                          slang_dict_path: Path = None,
                          vncorenlp_path: Path = None,
                          segmentation_method: str = 'pyvi'):
    """
    Tiền xử lý tất cả các splits (train/val/test)
    
    Args:
        data_dir: Thư mục chứa dữ liệu gốc
        output_dir: Thư mục output
        slang_dict_path: Đường dẫn từ điển slang
        vncorenlp_path: Đường dẫn đến VnCoreNLP JAR file
        segmentation_method: Phương pháp tách từ ('pyvi' hoặc 'vncorenlp')
    """
    print("\n" + "=" * 80)
    print("PREPROCESSING ALL DATA SPLITS")
    print("=" * 80)
    
    # Files to process
    files_to_process = [
        ('train_merged.csv', 'train.csv'),
        ('val.csv', 'val.csv'),
        ('test.csv', 'test.csv'),
    ]
    
    results = {}
    
    for input_name, output_name in files_to_process:
        input_file = data_dir / input_name
        
        if not input_file.exists():
            print(f"\n⚠️  File not found: {input_file}")
            continue
        
        output_file = output_dir / output_name
        
        try:
            df_processed = preprocess_file(
                input_file=input_file,
                output_file=output_file,
                text_column='Sentence',
                label_column='Emotion',
                slang_dict_path=slang_dict_path,
                word_segmentation=True,
                min_word_count=3,
                save_stats=True,
                vncorenlp_path=vncorenlp_path,
                segmentation_method=segmentation_method
            )
            
            results[output_name] = {
                'rows': len(df_processed),
                'status': 'success'
            }
            
        except Exception as e:
            print(f"\n❌ Error processing {input_name}: {e}")
            results[output_name] = {
                'rows': 0,
                'status': 'failed',
                'error': str(e)
            }
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    for filename, result in results.items():
        status_icon = "✅" if result['status'] == 'success' else "❌"
        print(f"{status_icon} {filename}: {result['rows']} rows ({result['status']})")
    
    total_rows = sum(r['rows'] for r in results.values() if r['status'] == 'success')
    print(f"\n📊 Total processed rows: {total_rows:,}")
    print(f"✅ Output directory: {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Tiền xử lý dữ liệu cho PhoBERT Sentiment Analysis"
    )
    
    parser.add_argument(
        '--input',
        type=str,
        help='Đường dẫn file input (CSV hoặc Excel)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        help='Đường dẫn file output (CSV)'
    )
    
    parser.add_argument(
        '--input-dir',
        type=str,
        help='Thư mục chứa dữ liệu raw (xử lý tất cả train/val/test)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        help='Thư mục output cho dữ liệu đã xử lý'
    )
    
    parser.add_argument(
        '--slang-dict',
        type=str,
        default='data/processed/slang_example.csv',
        help='Đường dẫn đến từ điển slang (default: data/processed/slang_example.csv)'
    )
    
    parser.add_argument(
        '--text-column',
        type=str,
        default='Sentence',
        help='Tên cột chứa văn bản (default: Sentence)'
    )
    
    parser.add_argument(
        '--label-column',
        type=str,
        default='Emotion',
        help='Tên cột chứa nhãn (default: Emotion)'
    )
    
    parser.add_argument(
        '--min-words',
        type=int,
        default=3,
        help='Số từ tối thiểu (default: 3)'
    )
    
    parser.add_argument(
        '--no-segmentation',
        action='store_true',
        help='Không thực hiện tách từ'
    )
    
    parser.add_argument(
        '--vncorenlp-path',
        type=str,
        help='Đường dẫn đến VnCoreNLP JAR file (nếu muốn dùng VnCoreNLP thay vì PyVi)'
    )
    
    parser.add_argument(
        '--segmentation-method',
        type=str,
        choices=['pyvi', 'vncorenlp'],
        default='pyvi',
        help='Phương pháp tách từ (default: pyvi)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.input and args.output:
        # Single file mode
        input_file = Path(args.input)
        output_file = Path(args.output)
        
        if not input_file.exists():
            print(f"❌ Input file not found: {input_file}")
            return
        
        slang_dict_path = Path(args.slang_dict) if args.slang_dict else None
        vncorenlp_path = Path(args.vncorenlp_path) if args.vncorenlp_path else None
        
        preprocess_file(
            input_file=input_file,
            output_file=output_file,
            text_column=args.text_column,
            label_column=args.label_column,
            slang_dict_path=slang_dict_path,
            word_segmentation=not args.no_segmentation,
            min_word_count=args.min_words,
            save_stats=True,
            vncorenlp_path=vncorenlp_path,
            segmentation_method=args.segmentation_method
        )
        
    elif args.input_dir and args.output_dir:
        # Batch mode: process all splits
        data_dir = Path(args.input_dir)
        output_dir = Path(args.output_dir)
        
        if not data_dir.exists():
            print(f"❌ Input directory not found: {data_dir}")
            return
        
        slang_dict_path = Path(args.slang_dict) if args.slang_dict else None
        vncorenlp_path = Path(args.vncorenlp_path) if args.vncorenlp_path else None
        
        preprocess_all_splits(
            data_dir=data_dir,
            output_dir=output_dir,
            slang_dict_path=slang_dict_path,
            vncorenlp_path=vncorenlp_path,
            segmentation_method=args.segmentation_method
        )
        
    else:
        print("❌ Error: Phải cung cấp (--input và --output) HOẶC (--input-dir và --output-dir)")
        parser.print_help()
        return
    
    print("\n✅ DONE!")


if __name__ == "__main__":
    main()

