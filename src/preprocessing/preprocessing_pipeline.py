"""
Preprocessing Pipeline
======================
Pipeline tích hợp đầy đủ cho tiền xử lý văn bản tiếng Việt.

Quy trình:
1. Text Cleaning (Làm sạch)
2. Emoji Conversion (Chuyển emoji)
3. Text Normalization (Chuẩn hóa slang/teencode)
4. Word Segmentation (Tách từ)
5. Final Cleanup & Filtering (Làm sạch cuối và lọc)

Author: PPNCKH Project
"""

import re
from pathlib import Path
from typing import Optional, Union, Literal
import pandas as pd

from .text_cleaner import TextCleaner
from .emoji_handler import EmojiHandler
from .text_normalizer import TextNormalizer
from .word_segmenter import WordSegmenter, SimpleWordSegmenter, PYVI_AVAILABLE


class PreprocessingPipeline:
    """
    Pipeline tiền xử lý hoàn chỉnh cho PhoBERT Sentiment Analysis.
    
    Tự động thực hiện tất cả các bước tiền xử lý theo đúng thứ tự.
    """
    
    def __init__(self,
                 slang_dict_path: Optional[Union[str, Path]] = None,
                 word_segmentation: bool = True,
                 segmentation_method: Literal['pyvi', 'vncorenlp', 'simple'] = 'vncorenlp',
                 vncorenlp_path: Optional[str] = None,
                 min_word_count: int = 3,
                 lowercase: bool = True):
        """
        Args:
            slang_dict_path: Đường dẫn đến từ điển slang/teencode
            word_segmentation: Có thực hiện tách từ không
            segmentation_method: Phương pháp tách từ ('pyvi', 'vncorenlp', 'simple')
            vncorenlp_path: Đường dẫn VnCoreNLP jar (nếu dùng vncorenlp)
            min_word_count: Số từ tối thiểu sau khi tách (để filter)
            lowercase: Có chuyển về chữ thường không
        """
        # Initialize các modules
        self.text_cleaner = TextCleaner()
        self.emoji_handler = EmojiHandler()
        self.text_normalizer = TextNormalizer(slang_dict_path=slang_dict_path)
        
        # Word segmentation
        self.word_segmentation = word_segmentation
        self.segmentation_method = segmentation_method
        
        if word_segmentation:
            if segmentation_method == 'simple':
                self.word_segmenter = SimpleWordSegmenter()
            else:
                try:
                    self.word_segmenter = WordSegmenter(
                        method=segmentation_method,
                        vncorenlp_path=vncorenlp_path
                    )
                except Exception as e:
                    print(f"⚠️  Failed to initialize {segmentation_method}: {e}")
                    print("    Falling back to PyVi if available, else SimpleWordSegmenter")
                    if PYVI_AVAILABLE:
                        try:
                            self.word_segmenter = WordSegmenter(method='pyvi')
                            print("    ✓ Using PyVi as fallback")
                        except:
                            self.word_segmenter = SimpleWordSegmenter()
                            print("    ✓ Using SimpleWordSegmenter as fallback")
                    else:
                        self.word_segmenter = SimpleWordSegmenter()
                        print("    ✓ Using SimpleWordSegmenter as fallback")
        
        # Settings
        self.min_word_count = min_word_count
        self.lowercase = lowercase
        
        print("✓ Preprocessing pipeline initialized")
    
    def preprocess(self, text: str, return_stats: bool = False) -> Union[str, tuple]:
        """
        Tiền xử lý văn bản - Pipeline đầy đủ
        
        Args:
            text: Văn bản đầu vào
            return_stats: Có trả về thống kê không
            
        Returns:
            Văn bản đã tiền xử lý (và stats nếu return_stats=True)
        """
        if not text or not isinstance(text, str):
            return ("", {"status": "empty_input"}) if return_stats else ""
        
        original_text = text
        stats = {
            "original_length": len(text),
            "original_words": len(text.split()),
        }
        
        # ===== BƯỚC 1: TEXT CLEANING =====
        text = self.text_cleaner.clean(
            text,
            remove_hashtags=True,
            keep_hashtag_text=True,
            reduce_chars=True,
            max_char_repeat=2,
            normalize_punct=True
        )
        
        if not text.strip():
            stats["status"] = "empty_after_cleaning"
            return ("", stats) if return_stats else ""
        
        stats["after_cleaning_length"] = len(text)
        
        # ===== BƯỚC 2: EMOJI CONVERSION =====
        text = self.emoji_handler.convert(text)
        stats["after_emoji_length"] = len(text)
        
        # ===== BƯỚC 3: TEXT NORMALIZATION =====
        text = self.text_normalizer.normalize(text)
        stats["after_normalization_length"] = len(text)
        
        # ===== BƯỚC 4: WORD SEGMENTATION =====
        if self.word_segmentation and self.word_segmenter:
            text = self.word_segmenter.segment(text)
            stats["after_segmentation_length"] = len(text)
        
        # ===== BƯỚC 5: FINAL CLEANUP =====
        # Lowercase
        if self.lowercase:
            text = text.lower()
        
        # Chuẩn hóa khoảng trắng cuối cùng
        text = ' '.join(text.split())
        
        # Kiểm tra độ dài tối thiểu
        word_count = len(text.split())
        stats["final_word_count"] = word_count
        stats["final_length"] = len(text)
        
        if word_count < self.min_word_count:
            stats["status"] = "too_short"
            return ("", stats) if return_stats else ""
        
        stats["status"] = "success"
        
        if return_stats:
            return text, stats
        return text
    
    def preprocess_batch(self, texts: list[str], 
                         show_progress: bool = True,
                         return_stats: bool = False) -> Union[list[str], tuple]:
        """
        Tiền xử lý nhiều văn bản
        
        Args:
            texts: List các văn bản
            show_progress: Hiển thị progress
            return_stats: Trả về statistics
            
        Returns:
            List văn bản đã xử lý (và stats nếu return_stats=True)
        """
        results = []
        stats_list = []
        
        total = len(texts)
        for i, text in enumerate(texts, 1):
            if show_progress and i % 100 == 0:
                print(f"Processing: {i}/{total} ({i/total*100:.1f}%)")
            
            if return_stats:
                result, stats = self.preprocess(text, return_stats=True)
                results.append(result)
                stats_list.append(stats)
            else:
                result = self.preprocess(text)
                results.append(result)
        
        if show_progress:
            print(f"✓ Completed: {total}/{total} (100%)")
        
        if return_stats:
            return results, stats_list
        return results
    
    def preprocess_dataframe(self, 
                            df: pd.DataFrame,
                            text_column: str = 'Sentence',
                            output_column: str = 'Sentence_processed',
                            keep_original: bool = True,
                            filter_invalid: bool = True) -> pd.DataFrame:
        """
        Tiền xử lý DataFrame
        
        Args:
            df: DataFrame chứa văn bản
            text_column: Tên cột chứa text gốc
            output_column: Tên cột output
            keep_original: Giữ cột gốc không
            filter_invalid: Lọc bỏ rows không hợp lệ (empty/too short)
            
        Returns:
            DataFrame đã xử lý
        """
        print(f"Processing DataFrame with {len(df)} rows...")
        
        # Xử lý
        results, stats_list = self.preprocess_batch(
            df[text_column].astype(str).tolist(),
            show_progress=True,
            return_stats=True
        )
        
        # Tạo DataFrame mới
        df_processed = df.copy()
        df_processed[output_column] = results
        
        # Thêm stats columns (optional)
        df_processed['preprocessing_status'] = [s['status'] for s in stats_list]
        df_processed['word_count'] = [s.get('final_word_count', 0) for s in stats_list]
        
        # Filter invalid rows
        if filter_invalid:
            original_len = len(df_processed)
            df_processed = df_processed[df_processed['preprocessing_status'] == 'success'].copy()
            filtered_count = original_len - len(df_processed)
            print(f"✓ Filtered {filtered_count} invalid rows ({filtered_count/original_len*100:.1f}%)")
        
        # Remove original column nếu không giữ
        if not keep_original and text_column != output_column:
            df_processed = df_processed.drop(columns=[text_column])
        
        print(f"✓ Final dataset: {len(df_processed)} rows")
        
        return df_processed
    
    def get_pipeline_info(self) -> dict:
        """Lấy thông tin về pipeline configuration"""
        return {
            "word_segmentation": self.word_segmentation,
            "segmentation_method": self.segmentation_method if self.word_segmentation else None,
            "min_word_count": self.min_word_count,
            "lowercase": self.lowercase,
            "slang_dict_size": len(self.text_normalizer.slang_dict),
            "emoji_dict_size": len(self.emoji_handler.emoji_dict),
            "emoticon_dict_size": len(self.emoji_handler.emoticon_dict),
        }


# ============================================================================
# DEMO & TESTING
# ============================================================================

def demo():
    """Demo preprocessing pipeline"""
    
    # Khởi tạo pipeline
    pipeline = PreprocessingPipeline(
        word_segmentation=True,
        segmentation_method='pyvi',
        min_word_count=3,
        lowercase=True
    )
    
    print("=" * 80)
    print("PREPROCESSING PIPELINE DEMO")
    print("=" * 80)
    print("\nPipeline Info:")
    for key, value in pipeline.get_pipeline_info().items():
        print(f"  {key}: {value}")
    
    # Test cases
    test_cases = [
        "Shop này okeeee lắm 😍😍 free ship nữa :))) ib nha @user https://abc.com",
        "Sảnnn phẩmmmm rấtttt tệ!!!! Ko muốn mua nữaaaa 😡😡😡",
        "Giá hợp lý, chất lượng tốt ⭐⭐⭐⭐⭐ #recommend #5sao",
        "Haizzzzz thất vọngggg quáaaaa 😭😭 đừng mua nhaaaa",
        "Ok nha bạn :)) giao hàng nhanh, đóng gói cẩn thận 👍",
        "Fake hàng à??? Ko auth 😠 rep đi shop",
        "OMG 😲 sp đẹp wa, tui mún order",
        "Dịch vụ cx bth thoi, k có j đặc biệt",
        "T thích lắm <3 sẽ mua lại",
        "A",  # Too short
    ]
    
    print("\n" + "=" * 80)
    print("SINGLE TEXT PROCESSING")
    print("=" * 80)
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n【Test {i}】")
        print(f"Input:  {text}")
        
        result, stats = pipeline.preprocess(text, return_stats=True)
        
        print(f"Output: {result if result else '[FILTERED]'}")
        print(f"Stats:  {stats['status']} | Words: {stats.get('final_word_count', 0)}")
    
    # Batch processing
    print("\n" + "=" * 80)
    print("BATCH PROCESSING")
    print("=" * 80)
    
    results = pipeline.preprocess_batch(test_cases, show_progress=False)
    
    valid_count = sum(1 for r in results if r)
    print(f"\nTotal: {len(test_cases)} | Valid: {valid_count} | Filtered: {len(test_cases) - valid_count}")
    
    # DataFrame processing
    print("\n" + "=" * 80)
    print("DATAFRAME PROCESSING")
    print("=" * 80)
    
    df_test = pd.DataFrame({
        'id': range(1, len(test_cases) + 1),
        'Sentence': test_cases,
        'Emotion': ['Enjoyment'] * len(test_cases)
    })
    
    df_processed = pipeline.preprocess_dataframe(
        df_test,
        text_column='Sentence',
        output_column='Sentence_processed',
        keep_original=True,
        filter_invalid=True
    )
    
    print(f"\n{df_processed[['Sentence', 'Sentence_processed', 'preprocessing_status']].head(10)}")


def compare_methods():
    """So sánh các phương pháp tách từ"""
    
    test_text = "Sản phẩm này chất lượng tốt, giao hàng nhanh, dịch vụ khách hàng tuyệt vời"
    
    print("=" * 80)
    print("SO SÁNH CÁC PHƯƠNG PHÁP TÁCH TỪ")
    print("=" * 80)
    print(f"\nText gốc: {test_text}")
    
    methods = ['simple', 'pyvi']
    
    for method in methods:
        try:
            pipeline = PreprocessingPipeline(
                word_segmentation=True,
                segmentation_method=method
            )
            result = pipeline.preprocess(test_text)
            print(f"\n【{method.upper()}】")
            print(f"  {result}")
        except Exception as e:
            print(f"\n【{method.upper()}】")
            print(f"  Error: {e}")


if __name__ == "__main__":
    demo()
    print("\n" + "=" * 80)
    compare_methods()

