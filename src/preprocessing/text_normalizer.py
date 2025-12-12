"""
Text Normalizer Module
======================
Chuẩn hóa teencode, slang, từ viết tắt và từ tiếng Anh sang tiếng Việt.

Author: PPNCKH Project
"""

import re
import pandas as pd
from pathlib import Path
from typing import Dict, Optional, Union


class TextNormalizer:
    """
    Chuẩn hóa văn bản tiếng Việt: slang, teencode, viết tắt, tiếng Anh phổ biến.
    """
    
    def __init__(self, slang_dict_path: Optional[Union[str, Path]] = None):
        """
        Args:
            slang_dict_path: Đường dẫn đến file CSV chứa từ điển slang
                            Format: slang,meaning (2 cột)
        """
        # Từ điển slang/teencode mặc định
        self.slang_dict = {
            # Đại từ
            'm': 'mình',
            'mk': 'mình',
            'mik': 'mình',
            't': 'tôi',
            'tui': 'tôi',
            'tớ': 'tôi',
            'tao': 'tao',
            'mày': 'mày',
            'nó': 'nó',
            'ta': 'ta',
            'cj': 'chị',
            'ck': 'chồng',
            'vk': 'vợ',
            'ny': 'người yêu',
            'bồ': 'người yêu',
            'crush': 'người thích',
            'bae': 'người yêu',
            'c': 'chị',
            'a': 'anh',
            'chế': 'chị',
            'e': 'em',
            'ông': 'ông',
            'bà': 'bà',
            'mẹ': 'mẹ',
            'bé': 'bé',
            
            # Phủ định / Khẳng định
            'ko': 'không',
            'k': 'không',
            'kg': 'không',
            'kh': 'không',
            'khong': 'không',
            'hok': 'không',
            'hong': 'không',
            'hemm': 'không',
            'dc': 'được',
            'đc': 'được',
            'ok': 'được',
            'oki': 'được',
            'oke': 'được',
            'okie': 'được',
            'okee': 'được',
            'dell': 'đéo',
            'cook': 'cút',
            
            # Từ thông dụng
            'vs': 'với',
            'v': 'vậy',
            'vc': 'vậy chứ',
            'vl': 'vậy luôn',
            'j': 'gì',
            'z': 'gì',
            'dzậy': 'vậy',
            'dzị': 'gì',
            'ntn': 'như thế nào',
            'sao': 'sao',
            'lm': 'làm',
            'lam': 'làm',
            'đc': 'được',
            'đk': 'được',
            'ms': 'mới',
            'mun': 'muốn',
            'muốn': 'muốn',
            'đi': 'đi',
            'di': 'đi',
            'cx': 'cũng',
            'cug': 'cũng',
            'cux': 'cũng',
            'nma': 'nhưng mà',
            'nhug': 'nhưng',
            'ma': 'mà',
            'mak': 'mà',
            'ak': 'à',
            'ạ': 'ạ',
            'nha': 'nhé',
            'nhe': 'nhé',
            'nka': 'nhé',
            'nhoa': 'nhé',
            'nki': 'nhé',
            'hen': 'hẹn',
            'heng': 'hẹn',
            'nhiu': 'nhiều',
            'nhìu': 'nhiều',
            'nhìu': 'nhiều',
            'r': 'rồi',
            'rùi': 'rồi',
            'rồi': 'rồi',
            'rui': 'rồi',
            'bik': 'biết',
            'bit': 'biết',
            'bít': 'biết',
            'biet': 'biết',
            'bỏ': 'bỏ',
            'bo': 'bỏ',
            'trog': 'trong',
            'trg': 'trong',
            'đag': 'đang',
            'dag': 'đang',
            'dg': 'đang',
            'dang': 'đang',
            
            # Cảm xúc / Đánh giá
            'tốt': 'tốt',
            'tot': 'tốt',
            'đep': 'đẹp',
            'dep': 'đẹp',
            'kém': 'kém',
            'kem': 'kém',
            'tệ': 'tệ',
            'te': 'tệ',
            'dỡ': 'dỡ',
            'do': 'dỡ',
            'xấu': 'xấu',
            'xau': 'xấu',
            'đỉnh': 'tuyệt',
            'dinh': 'tuyệt',
            'top': 'tốt nhất',
            'tuyệt': 'tuyệt',
            'tuyet': 'tuyệt',
            'tuyệt vời': 'tuyệt vời',
            'tuyet voi': 'tuyệt vời',
            'ổn': 'ổn',
            'on': 'ổn',
            'wow': 'tuyệt vời',
            'omg': 'ôi trời',
            'wtf': 'gì vậy',
            'lẻmon': 'chảnh',
            
            # Internet slang / Mạng xã hội
            'lol': 'cười',
            'lmao': 'cười',
            'rofl': 'cười lăn',
            'btw': 'nhân tiện',
            'imo': 'theo tôi',
            'imho': 'theo tôi',
            'fyi': 'cho bạn biết',
            'fb': 'facebook',
            'ig': 'instagram',
            'dm': 'nhắn tin',
            'pm': 'nhắn tin',
            'ib': 'nhắn tin',
            'inbox': 'nhắn tin',
            'rep': 'trả lời',
            'reply': 'trả lời',
            'cmt': 'bình luận',
            'comment': 'bình luận',
            'like': 'thích',
            'share': 'chia sẻ',
            'tag': 'gắn thẻ',
            'ad': 'quản trị viên',
            'admin': 'quản trị viên',
            'slay': 'sang',
            'per': 'người',
            
            # E-commerce slang
            'sp': 'sản phẩm',
            'san pham': 'sản phẩm',
            'shop': 'cửa hàng',
            'store': 'cửa hàng',
            'ship': 'vận chuyển',
            'shipper': 'người giao hàng',
            'shipping': 'vận chuyển',
            'free ship': 'miễn phí vận chuyển',
            'freeship': 'miễn phí vận chuyển',
            'cod': 'thanh toán khi nhận hàng',
            'cash on delivery': 'thanh toán khi nhận hàng',
            'voucher': 'phiếu giảm giá',
            'sale': 'giảm giá',
            'deal': 'ưu đãi',
            'flash sale': 'giảm giá nhanh',
            'order': 'đặt hàng',
            'checkout': 'thanh toán',
            'cart': 'giỏ hàng',
            'review': 'đánh giá',
            'rate': 'đánh giá',
            'rating': 'đánh giá',
            'refund': 'hoàn tiền',
            'return': 'trả hàng',
            'fake': 'giả',
            'real': 'thật',
            'auth': 'chính hãng',
            'authentic': 'chính hãng',
            'rep': 'hàng nhái',
            'replica': 'hàng nhái',
            'fullbox': 'đầy đủ hộp',
            'likenew': 'như mới',
            'brandnew': 'mới hoàn toàn',
            'secondhand': 'đã qua sử dụng',
            '2hand': 'đã qua sử dụng',
            
            # Viết tắt chung
            'vd': 'ví dụ',
            'vn': 'Việt Nam',
            'tphcm': 'Thành phố Hồ Chí Minh',
            'hn': 'Hà Nội',
            'sdt': 'số điện thoại',
            'đt': 'điện thoại',
            'dt': 'điện thoại',
            'sđt': 'số điện thoại',
            'qt': 'quá trời',
            'qá': 'quá',
            'wa': 'quá',
            'wá': 'quá',
            'vkl': 'vãi',
            'vcl': 'vãi',
            'vl': 'vãi',
            'cc': 'rất',
            'vcc': 'rất',
            'clgt': 'chúa lừa gà tàu',
            'tqt': 'tuyệt quá trời',
            'đtt': 'đỉnh thật',
            'nch': 'nói chung',
            'nc': 'nói chuyện',
            'bth': 'bình thường',
            'bt': 'bình thường',
            'tl': 'trả lời',
            'tldr': 'tóm tắt',
            'aka': 'còn gọi là',
            
            # Từ phổ biến khác
            'vãi': 'quá',
            'ác': 'ghê',
            'lắm': 'nhiều',
            'mấy': 'bao nhiêu',
            'đó': 'kia',
            'đấy': 'kia',
            'giờ': 'bây giờ',
        }
        
        # Load từ điển từ file nếu có
        if slang_dict_path:
            self.load_slang_dict(slang_dict_path)
        
        # Compile patterns cho hiệu suất
        self._compile_patterns()
    
    def load_slang_dict(self, file_path: Union[str, Path]):
        """
        Load từ điển slang từ file CSV
        
        Args:
            file_path: Đường dẫn đến file CSV (format: slang,meaning)
        """
        try:
            df = pd.read_csv(file_path, encoding='utf-8-sig')
            
            # Kiểm tra columns
            if 'slang' not in df.columns or 'meaning' not in df.columns:
                print(f"Warning: CSV file phải có 2 cột 'slang' và 'meaning'")
                return
            
            # Merge vào từ điển hiện tại (ưu tiên từ file)
            for _, row in df.iterrows():
                slang = str(row['slang']).strip().lower()
                meaning = str(row['meaning']).strip().lower()
                if slang and meaning:
                    self.slang_dict[slang] = meaning
            
            print(f"✓ Loaded {len(df)} slang terms from {file_path}")
            
        except Exception as e:
            print(f"Error loading slang dict from {file_path}: {e}")
    
    def _compile_patterns(self):
        """Compile regex patterns cho hiệu suất"""
        # Sắp xếp theo độ dài giảm dần (match cụm từ dài trước)
        sorted_keys = sorted(self.slang_dict.keys(), key=len, reverse=True)
        
        # Tạo pattern với word boundaries
        # \b không hoạt động tốt với tiếng Việt, dùng lookahead/lookbehind
        patterns = []
        for key in sorted_keys:
            # Escape special regex chars
            escaped = re.escape(key)
            # Pattern: phải là từ độc lập (không phải part của từ khác)
            pattern = r'(?<!\w)' + escaped + r'(?!\w)'
            patterns.append(pattern)
        
        self.pattern = re.compile('|'.join(patterns), flags=re.IGNORECASE | re.UNICODE)
    
    def normalize(self, text: str) -> str:
        """
        Chuẩn hóa văn bản: thay slang/teencode bằng từ chuẩn
        
        Args:
            text: Văn bản đầu vào
            
        Returns:
            Văn bản đã chuẩn hóa
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Lowercase để match (nhưng giữ nguyên output)
        def replace_func(match):
            matched_text = match.group(0)
            key = matched_text.lower()
            return self.slang_dict.get(key, matched_text)
        
        return self.pattern.sub(replace_func, text)
    
    def add_slang(self, slang: str, meaning: str):
        """
        Thêm slang mới vào từ điển
        
        Args:
            slang: Từ slang
            meaning: Nghĩa chuẩn
        """
        self.slang_dict[slang.lower()] = meaning.lower()
        self._compile_patterns()  # Rebuild patterns
    
    def remove_slang(self, slang: str):
        """Xóa slang khỏi từ điển"""
        if slang.lower() in self.slang_dict:
            del self.slang_dict[slang.lower()]
            self._compile_patterns()


# ============================================================================
# DEMO & TESTING
# ============================================================================

def demo():
    """Demo các chức năng của TextNormalizer"""
    
    normalizer = TextNormalizer()
    
    test_cases = [
        "Shop này ok lắm m thích",
        "Sp đẹp quá ko có gì để chê",
        "Free ship nhanh lắm nha, ib shop nhé",
        "Fake hàng à, k mua nữa đâu",
        "Auth ko vậy shop? Tui mún order",
        "Đc giảm giá k shop ơi, cj muốn mua nhìu",
        "Sp đẹpppp wa, rep nhanh, ship nhanhhh",
        "Tệ vl, k đáng tiền, đừng mua",
        "OMG đep qá, top 1 luôn",
        "Bth thoi, cx dc",
    ]
    
    print("=" * 80)
    print("TEXT NORMALIZER DEMO")
    print("=" * 80)
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n【Test {i}】")
        print(f"  Input:  {text}")
        normalized = normalizer.normalize(text)
        print(f"  Output: {normalized}")
    
    # Statistics
    print("\n" + "=" * 80)
    print(f"Tổng số slang trong từ điển: {len(normalizer.slang_dict)}")
    
    # Test với external dict
    print("\n" + "=" * 80)
    print("TEST VỚI EXTERNAL DICTIONARY")
    print("=" * 80)
    
    # Giả sử có file slang
    slang_file = Path(__file__).parent.parent.parent / "data" / "processed" / "slang_example.csv"
    if slang_file.exists():
        normalizer_ext = TextNormalizer(slang_dict_path=slang_file)
        print(f"Loaded dictionary with {len(normalizer_ext.slang_dict)} terms")
        
        test_text = "Sp này ok lắm, shop rep nhanh, free ship nữa"
        print(f"\nInput:  {test_text}")
        print(f"Output: {normalizer_ext.normalize(test_text)}")
    else:
        print(f"File không tồn tại: {slang_file}")


if __name__ == "__main__":
    demo()

