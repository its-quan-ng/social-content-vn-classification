"""
Text Cleaner Module
===================
Làm sạch văn bản: loại bỏ URL, email, phone, HTML, mentions, hashtags, 
chuẩn hóa Unicode, và rút gọn ký tự lặp.

Author: PPNCKH Project
"""

import re
import unicodedata
from typing import Optional


class TextCleaner:
    """
    Làm sạch văn bản tiếng Việt từ mạng xã hội.
    
    Các chức năng:
    - Loại bỏ URL, email, số điện thoại
    - Loại bỏ HTML tags
    - Loại bỏ mentions (@username), hashtags (#tag)
    - Chuẩn hóa Unicode (NFD → NFC)
    - Rút gọn ký tự lặp ("đẹppppp" → "đẹp")
    - Chuẩn hóa khoảng trắng
    """
    
    def __init__(self):
        # Regex patterns
        self.url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
        self.email_pattern = re.compile(r'\S+@\S+\.\S+')
        self.phone_pattern = re.compile(r'(?:\+84|0)[0-9]{9,10}')
        self.html_pattern = re.compile(r'<[^>]+>')
        self.mention_pattern = re.compile(r'@\w+')
        self.hashtag_pattern = re.compile(r'#\w+')
        
        # Pattern cho ký tự lặp (giữ tối đa 2 ký tự giống nhau)
        # "đẹppppp" → "đẹpp" → sau đó có thể rút về "đẹp"
        self.repeated_char_pattern = re.compile(r'(.)\1{2,}')
        
        # Pattern cho dấu câu lặp
        self.repeated_punct_pattern = re.compile(r'([!?.]){2,}')
        
    def remove_urls(self, text: str) -> str:
        """Loại bỏ URLs"""
        return self.url_pattern.sub('', text)
    
    def remove_emails(self, text: str) -> str:
        """Loại bỏ email addresses"""
        return self.email_pattern.sub('', text)
    
    def remove_phone_numbers(self, text: str) -> str:
        """Loại bỏ số điện thoại"""
        return self.phone_pattern.sub('', text)
    
    def remove_html_tags(self, text: str) -> str:
        """Loại bỏ HTML tags"""
        return self.html_pattern.sub('', text)
    
    def remove_mentions(self, text: str) -> str:
        """Loại bỏ mentions (@username)"""
        return self.mention_pattern.sub('', text)
    
    def remove_hashtags(self, text: str, keep_text: bool = True) -> str:
        """
        Xử lý hashtags
        
        Args:
            text: Văn bản đầu vào
            keep_text: Nếu True, giữ text của hashtag (bỏ dấu #)
                      Nếu False, xóa toàn bộ hashtag
        """
        if keep_text:
            # Chỉ bỏ dấu #, giữ lại text
            return self.hashtag_pattern.sub(lambda m: m.group(0)[1:], text)
        else:
            # Xóa toàn bộ
            return self.hashtag_pattern.sub('', text)
    
    def normalize_unicode(self, text: str) -> str:
        """
        Chuẩn hóa Unicode về dạng NFC
        NFD: é = e + ́ (2 ký tự)
        NFC: é (1 ký tự)
        """
        return unicodedata.normalize('NFC', text)
    
    def reduce_repeated_characters(self, text: str, max_repeat: int = 2) -> str:
        """
        Rút gọn ký tự lặp
        
        Args:
            text: Văn bản đầu vào
            max_repeat: Số lần lặp tối đa cho phép (mặc định = 2)
        
        Examples:
            "đẹppppp" → "đẹpp"
            "haaaaa" → "haa"
            "okeeee" → "okee"
        """
        return self.repeated_char_pattern.sub(r'\1' * max_repeat, text)
    
    def normalize_punctuation(self, text: str) -> str:
        """
        Chuẩn hóa dấu câu lặp
        
        Examples:
            "???" → "?"
            "!!!" → "!"
            "..." → "."
        """
        return self.repeated_punct_pattern.sub(r'\1', text)
    
    def normalize_whitespace(self, text: str) -> str:
        """
        Chuẩn hóa khoảng trắng:
        - Loại bỏ khoảng trắng đầu/cuối
        - Chuyển nhiều khoảng trắng thành 1
        - Loại bỏ newlines, tabs
        """
        # Chuyển newline, tab thành space
        text = re.sub(r'[\n\r\t]+', ' ', text)
        # Nhiều spaces → 1 space
        text = re.sub(r'\s+', ' ', text)
        # Trim
        return text.strip()
    
    def remove_special_characters(self, text: str, keep_punctuation: bool = True) -> str:
        """
        Loại bỏ ký tự đặc biệt
        
        Args:
            keep_punctuation: Nếu True, giữ dấu câu cơ bản (.,!?)
        """
        if keep_punctuation:
            # Chỉ giữ: chữ cái, số, khoảng trắng, dấu câu cơ bản
            text = re.sub(r'[^\w\s.,!?àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', ' ', text, flags=re.UNICODE)
        else:
            # Chỉ giữ chữ cái, số, khoảng trắng
            text = re.sub(r'[^\w\s]', ' ', text, flags=re.UNICODE)
        
        return text
    
    def clean(self, text: str, 
              remove_hashtags: bool = True,
              keep_hashtag_text: bool = True,
              reduce_chars: bool = True,
              max_char_repeat: int = 2,
              normalize_punct: bool = True) -> str:
        """
        Làm sạch văn bản - Pipeline đầy đủ
        
        Args:
            text: Văn bản đầu vào
            remove_hashtags: Có xử lý hashtags không
            keep_hashtag_text: Giữ text của hashtag (chỉ bỏ dấu #)
            reduce_chars: Có rút gọn ký tự lặp không
            max_char_repeat: Số lần lặp tối đa cho phép
            normalize_punct: Có chuẩn hóa dấu câu không
        
        Returns:
            Văn bản đã làm sạch
        """
        if not text or not isinstance(text, str):
            return ""
        
        # 1. Chuẩn hóa Unicode trước tiên
        text = self.normalize_unicode(text)
        
        # 2. Loại bỏ URLs, emails, phones
        text = self.remove_urls(text)
        text = self.remove_emails(text)
        text = self.remove_phone_numbers(text)
        
        # 3. Loại bỏ HTML tags
        text = self.remove_html_tags(text)
        
        # 4. Loại bỏ mentions
        text = self.remove_mentions(text)
        
        # 5. Xử lý hashtags
        if remove_hashtags:
            text = self.remove_hashtags(text, keep_text=keep_hashtag_text)
        
        # 6. Rút gọn ký tự lặp
        if reduce_chars:
            text = self.reduce_repeated_characters(text, max_repeat=max_char_repeat)
        
        # 7. Chuẩn hóa dấu câu
        if normalize_punct:
            text = self.normalize_punctuation(text)
        
        # 8. Chuẩn hóa khoảng trắng (luôn thực hiện)
        text = self.normalize_whitespace(text)
        
        return text


# ============================================================================
# DEMO & TESTING
# ============================================================================

def demo():
    """Demo các chức năng của TextCleaner"""
    
    cleaner = TextCleaner()
    
    test_cases = [
        "Shop này okeeee lắm 😍😍 free ship nữa :))) ib nha @user https://abc.com",
        "Sảnnn phẩmmmm rấtttt tệ!!!! Ko muốn mua nữaaaa 😡😡😡",
        "Giá hợp lý, chất lượng tốt ⭐⭐⭐⭐⭐ #recommend #5sao",
        "<p>Đơn hàng của tôi đâu rồi???</p> Email: test@gmail.com - SĐT: 0123456789",
        "Haizzzzz thất vọngggg quáaaaa 😭😭 đừng mua nhaaaa",
    ]
    
    print("=" * 80)
    print("TEXT CLEANER DEMO")
    print("=" * 80)
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n【Test {i}】")
        print(f"  Input:  {text}")
        
        # Làm sạch
        cleaned = cleaner.clean(text)
        print(f"  Output: {cleaned}")
        
        # Hiển thị từng bước
        print(f"\n  Chi tiết:")
        print(f"    1. Remove URLs:      {cleaner.remove_urls(text)}")
        print(f"    2. Remove mentions:  {cleaner.remove_mentions(text)}")
        print(f"    3. Reduce chars:     {cleaner.reduce_repeated_characters(text)}")
        print(f"    4. Clean (full):     {cleaned}")


if __name__ == "__main__":
    demo()

