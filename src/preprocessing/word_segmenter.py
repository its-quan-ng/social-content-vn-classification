"""
Word Segmenter Module
=====================
Tách từ tiếng Việt sử dụng VnCoreNLP hoặc PyVi.

PhoBERT được huấn luyện trên text đã tách từ, nên cần tách từ trước khi đưa vào model.

Author: PPNCKH Project
"""

import re
from typing import Optional, Literal

try:
    from pyvi import ViTokenizer
    PYVI_AVAILABLE = True
except ImportError:
    PYVI_AVAILABLE = False
    print("⚠️  PyVi not installed. Install with: pip install pyvi")

try:
    from vncorenlp import VnCoreNLP
    VNCORENLP_AVAILABLE = True
except ImportError:
    VNCORENLP_AVAILABLE = False
    print("⚠️  VnCoreNLP not installed. Install with: pip install vncorenlp")


class WordSegmenter:
    """
    Tách từ tiếng Việt cho PhoBERT.
    
    Hỗ trợ 2 thư viện:
    - PyVi: Nhẹ, nhanh, không cần Java (RECOMMENDED)
    - VnCoreNLP: Chính xác hơn nhưng nặng, cần Java
    """
    
    def __init__(self, 
                 method: Literal['pyvi', 'vncorenlp'] = 'vncorenlp',
                 vncorenlp_path: Optional[str] = None):
        """
        Args:
            method: Phương pháp tách từ ('pyvi' hoặc 'vncorenlp')
            vncorenlp_path: Đường dẫn đến VnCoreNLP jar file (nếu dùng vncorenlp)
        """
        self.method = method
        self.vncorenlp = None
        
        if method == 'pyvi':
            if not PYVI_AVAILABLE:
                raise ImportError("PyVi not installed. Install with: pip install pyvi")
            print("✓ Using PyVi for word segmentation")
            
        elif method == 'vncorenlp':
            if not VNCORENLP_AVAILABLE:
                raise ImportError("VnCoreNLP not installed. Install with: pip install vncorenlp")
            
            if not vncorenlp_path:
                raise ValueError("vncorenlp_path is required when using VnCoreNLP")
            
            try:
                # Convert Path object to string if needed
                from pathlib import Path
                if isinstance(vncorenlp_path, Path):
                    vncorenlp_path = str(vncorenlp_path)
                
                # Khởi tạo VnCoreNLP
                self.vncorenlp = VnCoreNLP(vncorenlp_path, annotators="wseg", max_heap_size='-Xmx2g')
                print("✓ Using VnCoreNLP for word segmentation")
            except Exception as e:
                raise RuntimeError(f"Failed to initialize VnCoreNLP: {e}")
        
        else:
            raise ValueError(f"Invalid method: {method}. Choose 'pyvi' or 'vncorenlp'")
    
    def segment(self, text: str) -> str:
        """
        Tách từ cho văn bản tiếng Việt
        
        Args:
            text: Văn bản đầu vào
            
        Returns:
            Văn bản đã tách từ (các từ nối bằng dấu _)
            
        Examples:
            "thực sự thất vọng" → "thực_sự thất_vọng"
            "sản phẩm chất lượng tốt" → "sản_phẩm chất_lượng tốt"
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Clean text trước khi tách từ
        text = text.strip()
        if not text:
            return ""
        
        try:
            if self.method == 'pyvi':
                return ViTokenizer.tokenize(text)
            
            elif self.method == 'vncorenlp':
                # VnCoreNLP trả về list of sentences, mỗi sentence là list of words
                sentences = self.vncorenlp.tokenize(text)
                # Join words with space, join sentences with space
                result = ' '.join([' '.join(sent) for sent in sentences])
                return result
        
        except Exception as e:
            print(f"Error during segmentation: {e}")
            return text  # Fallback: trả về text gốc
    
    def segment_batch(self, texts: list[str]) -> list[str]:
        """
        Tách từ cho nhiều văn bản cùng lúc
        
        Args:
            texts: List các văn bản
            
        Returns:
            List các văn bản đã tách từ
        """
        return [self.segment(text) for text in texts]
    
    def __del__(self):
        """Cleanup VnCoreNLP khi object bị destroy"""
        if self.vncorenlp:
            try:
                self.vncorenlp.close()
            except:
                pass


class SimpleWordSegmenter:
    """
    Tách từ đơn giản dựa trên regex (không cần thư viện bên ngoài).
    
    ⚠️  KHÔNG chính xác như PyVi/VnCoreNLP, chỉ dùng cho testing hoặc khi không có thư viện.
    """
    
    def __init__(self):
        # Danh sách các cụm từ phổ biến cần tách (không đầy đủ)
        self.compound_words = [
            'sản phẩm', 'chất lượng', 'dịch vụ', 'khách hàng', 'cửa hàng',
            'giá cả', 'mức giá', 'giao hàng', 'vận chuyển', 'đóng gói',
            'thực sự', 'thật sự', 'rất là', 'quá đỗi', 'hơi bị',
            'không thể', 'có thể', 'nên có', 'cần phải', 'phải có',
            'thất vọng', 'hài lòng', 'tuyệt vời', 'tốt nhất', 'xấu nhất',
            'miễn phí', 'thanh toán', 'đặt hàng', 'mua hàng', 'bán hàng',
            'người bán', 'người mua', 'người giao', 'nhân viên', 'quản lý',
        ]
        
        # Sort by length descending (match longer phrases first)
        self.compound_words.sort(key=len, reverse=True)
    
    def segment(self, text: str) -> str:
        """
        Tách từ đơn giản
        
        ⚠️  Chỉ nên dùng khi không có PyVi/VnCoreNLP
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Replace compound words with underscore version
        result = text
        for compound in self.compound_words:
            compound_with_underscore = compound.replace(' ', '_')
            # Case insensitive replacement
            pattern = re.compile(re.escape(compound), re.IGNORECASE)
            result = pattern.sub(compound_with_underscore, result)
        
        return result


# ============================================================================
# DEMO & TESTING
# ============================================================================

def demo():
    """Demo các chức năng của WordSegmenter"""
    
    test_cases = [
        "Sản phẩm này chất lượng tốt",
        "Dịch vụ khách hàng rất tệ",
        "Giao hàng nhanh, đóng gói cẩn thận",
        "Thực sự thất vọng với chất lượng",
        "Cửa hàng này bán hàng giá rẻ",
        "Không thể tin được sản phẩm tốt vậy",
        "Miễn phí vận chuyển rất hài lòng",
        "Người bán phục vụ tốt thanh toán dễ dàng",
    ]
    
    print("=" * 80)
    print("WORD SEGMENTER DEMO")
    print("=" * 80)
    
    # Try PyVi first
    if PYVI_AVAILABLE:
        print("\n【Using PyVi】")
        segmenter = WordSegmenter(method='pyvi')
        
        for i, text in enumerate(test_cases, 1):
            print(f"\n【Test {i}】")
            print(f"  Input:  {text}")
            segmented = segmenter.segment(text)
            print(f"  Output: {segmented}")
    
    else:
        print("\n⚠️  PyVi not available. Using SimpleWordSegmenter (fallback)")
        segmenter = SimpleWordSegmenter()
        
        for i, text in enumerate(test_cases, 1):
            print(f"\n【Test {i}】")
            print(f"  Input:  {text}")
            segmented = segmenter.segment(text)
            print(f"  Output: {segmented}")
    
    # Batch processing test
    print("\n" + "=" * 80)
    print("BATCH PROCESSING TEST")
    print("=" * 80)
    
    if PYVI_AVAILABLE:
        segmenter = WordSegmenter(method='pyvi')
        batch_texts = [
            "Sản phẩm tốt",
            "Dịch vụ tệ",
            "Giao hàng nhanh"
        ]
        results = segmenter.segment_batch(batch_texts)
        for text, result in zip(batch_texts, results):
            print(f"{text:30} → {result}")


def install_guide():
    """Hướng dẫn cài đặt"""
    print("""
    ╔════════════════════════════════════════════════════════════════════════╗
    ║                    HƯỚNG DẪN CÀI ĐẶT                                   ║
    ╚════════════════════════════════════════════════════════════════════════╝
    
    【Phương án 1: PyVi (RECOMMENDED)】
    ✅ Ưu điểm: Nhẹ, nhanh, không cần Java
    ❌ Nhược điểm: Độ chính xác thấp hơn VnCoreNLP
    
    Cài đặt:
        pip install pyvi
    
    Sử dụng:
        from word_segmenter import WordSegmenter
        segmenter = WordSegmenter(method='pyvi')
        result = segmenter.segment("sản phẩm tốt")
    
    ─────────────────────────────────────────────────────────────────────────
    
    【Phương án 2: VnCoreNLP】
    ✅ Ưu điểm: Chính xác cao hơn
    ❌ Nhược điểm: Nặng, cần Java, phức tạp
    
    Cài đặt:
        1. Cài Java (JRE >= 1.8): https://www.java.com/
        2. pip install vncorenlp
        3. Download VnCoreNLP: 
           https://github.com/vncorenlp/VnCoreNLP
        4. Extract file và lưu đường dẫn
    
    Sử dụng:
        segmenter = WordSegmenter(
            method='vncorenlp',
            vncorenlp_path='/path/to/VnCoreNLP/VnCoreNLP-1.1.1.jar'
        )
    
    ─────────────────────────────────────────────────────────────────────────
    
    【Phương án 3: Simple Segmenter (Fallback)】
    ⚠️  Chỉ dùng khi không có PyVi/VnCoreNLP
    
    Sử dụng:
        from word_segmenter import SimpleWordSegmenter
        segmenter = SimpleWordSegmenter()
        result = segmenter.segment("sản phẩm tốt")
    
    ═════════════════════════════════════════════════════════════════════════
    
    💡 Khuyến nghị: Dùng PyVi cho hầu hết trường hợp
    """)


if __name__ == "__main__":
    if PYVI_AVAILABLE or VNCORENLP_AVAILABLE:
        demo()
    else:
        print("\n⚠️  Không có thư viện tách từ nào được cài đặt!")
        install_guide()

