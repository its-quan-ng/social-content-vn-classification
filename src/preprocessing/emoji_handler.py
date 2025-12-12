"""
Emoji Handler Module
====================
Chuyển đổi emoji và emoticons sang từ tiếng Việt mô tả cảm xúc.

Author: PPNCKH Project
"""

import re
from typing import Dict, Optional


class EmojiHandler:
    """
    Chuyển đổi emoji Unicode và emoticons văn bản sang tiếng Việt.
    
    Giữ lại ngữ nghĩa cảm xúc thay vì xóa bỏ emoji.
    """
    
    def __init__(self):
        # Từ điển emoji Unicode → Tiếng Việt
        self.emoji_dict = {
            # 😊 Positive emotions
            '😀': 'cười',
            '😁': 'cười toe toét',
            '😂': 'cười',
            '🤣': 'cười lăn',
            '😃': 'cười',
            '😄': 'cười tươi',
            '😅': 'cười xấu hổ',
            '😆': 'cười toe toét',
            '😊': 'cười',
            '😇': 'vui vẻ',
            '🙂': 'mím cười',
            '🙃': 'cười',
            '😉': 'nháy mắt',
            '😌': 'nhẹ nhàng',
            '😍': 'thích thú yêu',
            '🥰': 'yêu thích',
            '😘': 'gửi nụ hôn',
            '😗': 'hôn',
            '😙': 'hôn',
            '😚': 'hôn',
            '😋': 'ngon',
            '😛': 'lè lưỡi',
            '😜': 'nháy mắt lè lưỡi',
            '🤪': 'điên',
            '😝': 'lè lưỡi',
            '🤑': 'tiền',
            '🤗': 'ôm',
            '🤭': 'che miệng',
            '🤩': 'ngưỡng mộ',
            '🥳': 'tiệc tung',
            
            # 😢 Sadness
            '😢': 'buồn',
            '😭': 'khóc',
            '😿': 'buồn',
            '😔': 'buồn bã',
            '😞': 'thất vọng',
            '😟': 'lo lắng',
            '😥': 'buồn',
            '😪': 'buồn ngủ',
            '🥺': 'van xin',
            '☹️': 'buồn',
            '🙁': 'buồn',
            
            # 😠 Anger
            '😠': 'tức giận',
            '😡': 'giận dữ',
            '🤬': 'chửi thề',
            '👿': 'ác quỷ',
            '💢': 'tức giận',
            
            # 🤢 Disgust
            '🤢': 'buồn nôn',
            '🤮': 'nôn mửa',
            '🤧': 'ốm',
            '😷': 'bệnh',
            '🤒': 'ốm',
            '🤕': 'đau',
            '💩': 'phân',
            
            # 😨 Fear
            '😨': 'sợ hãi',
            '😰': 'lo sợ',
            '😱': 'kinh hãi',
            '😖': 'khó chịu',
            '😣': 'khó khăn',
            '😓': 'mệt mỏi',
            '😩': 'mệt mỏi',
            '😫': 'mệt mỏi',
            
            # 😲 Surprise
            '😯': 'ngạc nhiên',
            '😲': 'ngạc nhiên',
            '😳': 'ngạc nhiên',
            '🤯': 'bùng nổ',
            '😮': 'ngạc nhiên',
            
            # ❤️ Hearts & Symbols
            '❤️': 'tim',
            '💕': 'tim',
            '💖': 'tim',
            '💗': 'tim',
            '💘': 'tim',
            '💙': 'tim',
            '💚': 'tim',
            '💛': 'tim',
            '🧡': 'tim',
            '💜': 'tim',
            '🖤': 'tim',
            '💝': 'quà tặng',
            '💞': 'tim',
            '💟': 'tim',
            '❣️': 'tim',
            '💔': 'tan vỡ',
            '♥️': 'tim',
            '💯': 'trăm điểm',
            '⭐': 'sao',
            '🌟': 'sao',
            '✨': 'lấp lánh',
            '🔥': 'lửa',
            '💥': 'bùng nổ',
            '💫': 'chóng mặt',
            '⚡': 'sét',
            
            # 👍 Gestures
            '👍': 'thích',
            '👎': 'không thích',
            '👏': 'vỗ tay',
            '🙏': 'cầu nguyện',
            '🤝': 'bắt tay',
            '👊': 'đấm',
            '✊': 'đấm',
            '🤛': 'đấm',
            '🤜': 'đấm',
            '🤞': 'may mắn',
            '✌️': 'chiến thắng',
            '🤟': 'yêu',
            '🤘': 'rock',
            '👌': 'ok',
            '🤌': 'ý kiến',
            '🤏': 'nhỏ',
            '👈': 'trái',
            '👉': 'phải',
            '👆': 'trên',
            '👇': 'dưới',
            '☝️': 'một',
            '✋': 'tay',
            '🤚': 'tay',
            '🖐️': 'tay',
            '🖖': 'chào',
            '👋': 'vẫy tay',
            '🤙': 'gọi',
            '💪': 'mạnh',
            '🦾': 'mạnh',
            '🙌': 'tay lên',
            '👐': 'mở',
            '🤲': 'cầu xin',
            
            # 🙈 Animals (có ý nghĩa)
            '🙈': 'không nhìn',
            '🙉': 'không nghe',
            '🙊': 'không nói',
            
            # Other useful
            '💀': 'chết',
            '☠️': 'chết',
            '👻': 'ma',
            '💤': 'ngủ',
            '💭': 'suy nghĩ',
            '💬': 'trò chuyện',
            '🗨️': 'nói',
            '🎉': 'ăn mừng',
            '🎊': 'ăn mừng',
            '🎈': 'bóng bay',
            '🎁': 'quà',
            '🔫': 'súng',
            '🔪': 'dao',
            
            # New emojis from dataset analysis
            '🥲': 'khóc',
            '🥹': 'xúc động',
            '😑': 'chán chường',
            '🙄': 'bất mãn',
            '😒': 'khó chịu',
            '🤡': 'ngớ ngẩn',
            '☺': 'cười',
            '🤔': 'suy nghĩ',
            '😏': 'cười thách thức',
            '😎': 'ngầu',
            '😐': 'cạn lời',
            '🤤': 'thèm',
            '🥵': 'nóng',
            '😬': 'sượng',
            '🥶': 'sợ',
            '😤': 'tức',
            '🐧': 'giỡn',
            '🐶': 'chó',
            '🧐': 'nghiêm túc',
            '😶': 'im lặng',
            '🗿': 'ngầu',
            '🥴': 'choáng váng',
            '😧': 'sốc',
            '😕': 'hoang mang',
            '😵': 'chóng mặt',
            '🤨': 'nghi ngờ',
            '🥀': 'hoa',
            '🤦': 'bó tay',
            '🚩': 'cảnh báo',
            '🌸': 'hoa',
            '🖕': 'chửi',
            '😈': 'quỷ',
            '✅': 'đúng',
            '🌝': 'mặt trăng',
            '😻': 'yêu thích',
            '💋': 'hôn',
            '💨': 'gió',
            '🍃': 'lá',
            '🙎': 'buồn',
            '💓': 'tim',
            '🐽': 'lợn',
            '🐷': 'lợn',
        }
        
        # Emoticons văn bản (text-based)
        self.emoticon_dict = {
            # Positive
            ':)': 'cười',
            ':))': 'cười',
            ':)))': 'cười',
            ':D': 'cười',
            '=)': 'cười',
            '=))': 'cười',
            '^_^': 'vui',
            '^.^': 'vui',
            '^^': 'vui',
            ':3': 'dễ thương',
            ':>': 'cười',
            ':v': 'cười xòa cho qua',
            ':V': 'cười xòa cho qua',
            ';)': 'nháy mắt',
            ';))': 'nháy mắt',
            '<3': 'tim',
            '♡': 'tim',
            '♥': 'tim',
            '=]': 'cười',
            ':]': 'cười',
            '>.<': 'khó chịu',
            
            # Negative  
            ':(': 'buồn',
            ':((': 'buồn',
            ':(((': 'buồn',
            '=(': 'buồn',
            '=((': 'buồn',
            ":'(": 'khóc',
            ":')": 'khóc',
            'T_T': 'khóc',
            'T.T': 'khóc',
            ';(': 'buồn',
            ';((': 'buồn',
            ':/': 'băn khoăn',
            ':\\': 'băn khoăn',
            ':|': 'thờ ơ',
            
            # Surprise/Other
            ':o': 'ngạc nhiên',
            ':O': 'ngạc nhiên',
            '=o': 'ngạc nhiên',
            '=O': 'ngạc nhiên',
            ':p': 'lè lưỡi',
            ':P': 'lè lưỡi',
            ';p': 'lè lưỡi',
            ';P': 'lè lưỡi',
            '^^;': 'xấu hổ',
            '>:(': 'tức giận',
            '>:((': 'tức giận',
            '-_-': 'mệt mỏi',
            '-.-': 'mệt mỏi',
            '>.>': 'nghi ngờ',
            '<.<': 'nghi ngờ',
            'XD': 'cười lớn',
            'xD': 'cười lớn',
        }
        
        # Tạo pattern cho emoticons (cần escape các ký tự đặc biệt)
        # Sắp xếp theo độ dài giảm dần để match pattern dài trước
        emoticon_patterns = sorted(self.emoticon_dict.keys(), key=len, reverse=True)
        emoticon_patterns_escaped = [re.escape(p) for p in emoticon_patterns]
        self.emoticon_pattern = re.compile('|'.join(emoticon_patterns_escaped))
        
        # Pattern cho emoticons với nhiều dấu lặp (VD: :))), =))))
        # Sẽ match và normalize về base form
        self.repeated_emoticon_patterns = {
            r':(\)+){2,}': ':))',      # :)), :))), :)))) → :))
            r'=(\)+){2,}': '=))',      # =)), =))), =)))) → =))
            r':(\(+){2,}': ':((',      # :((, :(((, :((((  → :((
            r'=(\(+){2,}': '=((',      # =((, =(((         → =((
            r';(\)+){2,}': ';))',      # ;)), ;))), ;))))  → ;))
        }
        
    def convert_emoticons(self, text: str) -> str:
        """
        Chuyển đổi emoticons văn bản thành tiếng Việt
        
        Args:
            text: Văn bản chứa emoticons
            
        Returns:
            Văn bản đã thay emoticons bằng từ tiếng Việt
            
        Example:
            ":))" → "cười"
            ":))))" → "cười"  (normalize về :))
            "Sản phẩm tốt :))" → "Sản phẩm tốt cười"
        """
        # Bước 1: Normalize các emoticons có nhiều dấu lặp về base form
        for pattern, replacement in self.repeated_emoticon_patterns.items():
            text = re.sub(pattern, replacement, text)
        
        # Bước 2: Thay thế emoticons bằng từ tiếng Việt
        def replace_emoticon(match):
            return self.emoticon_dict.get(match.group(0), match.group(0))
        
        return self.emoticon_pattern.sub(replace_emoticon, text)
    
    def convert_emoji(self, text: str) -> str:
        """
        Chuyển đổi emoji Unicode thành tiếng Việt
        
        Args:
            text: Văn bản chứa emoji
            
        Returns:
            Văn bản đã thay emoji bằng từ tiếng Việt
            
        Example:
            "😍😍" → "thích thú yêu thích thú yêu"
        """
        result = []
        for char in text:
            if char in self.emoji_dict:
                result.append(self.emoji_dict[char])
            else:
                result.append(char)
        
        return ' '.join(''.join(result).split())  # Chuẩn hóa khoảng trắng
    
    def convert(self, text: str) -> str:
        """
        Chuyển đổi cả emoji và emoticons
        
        Args:
            text: Văn bản đầu vào
            
        Returns:
            Văn bản đã chuyển đổi
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Thứ tự: Emoticons trước (vì có thể bị nhầm với ký tự khác)
        text = self.convert_emoticons(text)
        text = self.convert_emoji(text)
        
        return text
    
    def add_emoji(self, emoji: str, meaning: str):
        """Thêm emoji mới vào từ điển"""
        self.emoji_dict[emoji] = meaning
    
    def add_emoticon(self, emoticon: str, meaning: str):
        """Thêm emoticon mới vào từ điển"""
        self.emoticon_dict[emoticon] = meaning
        # Rebuild pattern
        emoticon_patterns = sorted(self.emoticon_dict.keys(), key=len, reverse=True)
        emoticon_patterns_escaped = [re.escape(p) for p in emoticon_patterns]
        self.emoticon_pattern = re.compile('|'.join(emoticon_patterns_escaped))


# ============================================================================
# DEMO & TESTING
# ============================================================================

def demo():
    """Demo các chức năng của EmojiHandler"""
    
    handler = EmojiHandler()
    
    test_cases = [
        "Sản phẩm này đẹp quá 😍😍😍",
        "Shop phục vụ tệ :((( không mua nữa",
        "Ok nha bạn :)) cảm ơn nhiều ❤️",
        "Thất vọng quá 😭😭 không như mong đợi",
        "Giận lắm rồi 😡😡 fake hàng",
        "Đóng gói cẩn thận 👍 ship nhanh 🚚",
        "Ngon quá =))) recommend 💯",
        "Sợ quá 😱 hàng nhái",
        "OMG 😲 giá rẻ vậy",
        "Yêu shop lắm <3 <3 ^^",
    ]
    
    print("=" * 80)
    print("EMOJI HANDLER DEMO")
    print("=" * 80)
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n【Test {i}】")
        print(f"  Input:  {text}")
        converted = handler.convert(text)
        print(f"  Output: {converted}")
    
    # Test riêng từng loại
    print("\n" + "=" * 80)
    print("CHI TIẾT: EMOJI vs EMOTICONS")
    print("=" * 80)
    
    test_emoji = "Tuyệt vời 😍 👍 ❤️"
    test_emoticon = "Tuyệt vời :)) <3"
    
    print(f"\n【Emoji Unicode】")
    print(f"  Input:  {test_emoji}")
    print(f"  Output: {handler.convert_emoji(test_emoji)}")
    
    print(f"\n【Emoticon Text】")
    print(f"  Input:  {test_emoticon}")
    print(f"  Output: {handler.convert_emoticons(test_emoticon)}")
    
    # Statistics
    print("\n" + "=" * 80)
    print(f"Tổng số emoji trong từ điển: {len(handler.emoji_dict)}")
    print(f"Tổng số emoticon trong từ điển: {len(handler.emoticon_dict)}")


if __name__ == "__main__":
    demo()

