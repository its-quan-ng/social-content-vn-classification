"""
Analyze Missing Tokens in Dataset
==================================
Scan train_merged.csv để tìm emoji và slang chưa có trong dictionary.

Author: PPNCKH Project
"""

import sys
import re
from pathlib import Path
from collections import Counter
import pandas as pd

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.preprocessing import EmojiHandler, TextNormalizer


def extract_emojis(text):
    """Trích xuất tất cả emoji từ text"""
    if not isinstance(text, str):
        return []
    
    # Emoji regex pattern
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U00002600-\U000026FF"  # Miscellaneous Symbols
        "\U00002700-\U000027BF"  # Dingbats
        "]+", 
        flags=re.UNICODE
    )
    
    return emoji_pattern.findall(text)


def extract_potential_slang(text):
    """Trích xuất các từ có thể là slang"""
    if not isinstance(text, str):
        return []
    
    # Lowercase
    text = text.lower()
    
    # Patterns cho teencode/slang:
    # - Từ có ký tự lặp: okkkk, đẹpppp
    # - Từ ngắn (1-2 ký tự): m, t, k, j
    # - Từ có số: 2hand, 4k
    # - Từ viết tắt: sp, dc, ko
    
    patterns = []
    
    # Từ có ký tự lặp liên tiếp (3+ lần)
    repeated = re.findall(r'\b\w*(\w)\1{2,}\w*\b', text)
    
    # Từ ngắn 1-3 ký tự (có thể là viết tắt)
    short_words = re.findall(r'\b[a-z]{1,3}\b', text)
    
    # Từ có số
    with_numbers = re.findall(r'\b\w*\d+\w*\b', text)
    
    return short_words + with_numbers


def analyze_dataset(csv_path: Path):
    """Phân tích dataset để tìm emoji và slang còn thiếu"""
    
    print("=" * 80)
    print("ANALYZING DATASET FOR MISSING TOKENS")
    print("=" * 80)
    
    # Load data
    print(f"\n📂 Loading {csv_path.name}...")
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    print(f"   Loaded {len(df)} rows")
    
    # Load existing dictionaries
    print("\n📚 Loading existing dictionaries...")
    emoji_handler = EmojiHandler()
    normalizer = TextNormalizer()
    
    print(f"   Emoji dict: {len(emoji_handler.emoji_dict)} emoji")
    print(f"   Emoticon dict: {len(emoji_handler.emoticon_dict)} emoticon")
    print(f"   Slang dict: {len(normalizer.slang_dict)} slang")
    
    # Extract all emojis from dataset
    print("\n🔍 Scanning for emojis...")
    all_emojis = []
    for text in df['Sentence']:
        if isinstance(text, str):
            emojis = extract_emojis(text)
            all_emojis.extend(emojis)
    
    # Count emoji frequency
    emoji_counter = Counter(all_emojis)
    print(f"   Found {len(emoji_counter)} unique emojis")
    print(f"   Total emoji occurrences: {sum(emoji_counter.values())}")
    
    # Find missing emojis
    missing_emojis = {}
    for emoji, count in emoji_counter.most_common():
        # Check each character in emoji string (some emojis are multi-char)
        for char in emoji:
            if char not in emoji_handler.emoji_dict and char not in emoji_handler.emoticon_dict:
                if char not in missing_emojis:
                    missing_emojis[char] = 0
                missing_emojis[char] += count
    
    print(f"\n❓ Missing emojis: {len(missing_emojis)}")
    if missing_emojis:
        print("\nTop 50 missing emojis (sorted by frequency):")
        print("-" * 80)
        for i, (emoji, count) in enumerate(sorted(missing_emojis.items(), key=lambda x: x[1], reverse=True)[:50], 1):
            # Show emoji with unicode code point
            code_point = f"U+{ord(emoji):04X}"
            print(f"{i:3}. {emoji}  ({code_point}) - appears {count:,} times")
    
    # Extract potential slang
    print("\n\n🔍 Scanning for potential slang/teencode...")
    all_words = []
    for text in df['Sentence']:
        if isinstance(text, str):
            # Clean text first
            text = text.lower()
            # Extract words
            words = re.findall(r'\b\w+\b', text)
            all_words.extend(words)
    
    word_counter = Counter(all_words)
    print(f"   Found {len(word_counter)} unique words")
    print(f"   Total words: {sum(word_counter.values()):,}")
    
    # Find potential missing slang
    # Criteria: short words (1-4 chars), frequent (>50 times), not in dict
    potential_slang = {}
    for word, count in word_counter.most_common():
        # Skip if already in dict
        if word in normalizer.slang_dict:
            continue
        
        # Check criteria
        is_short = len(word) <= 4
        is_frequent = count >= 50
        has_repeated = re.search(r'(.)\1{2,}', word)  # ký tự lặp
        
        # Common Vietnamese words to skip
        common_vietnamese = ['của', 'này', 'được', 'không', 'cho', 'mua', 'nhà', 
                            'rất', 'thì', 'đến', 'có', 'nào', 'như', 'với', 'đã',
                            'một', 'làm', 'khi', 'nhé', 'nha', 'ạ', 'à', 'ơi',
                            'thế', 'mình', 'tôi', 'bạn', 'anh', 'chị', 'em']
        
        if word in common_vietnamese:
            continue
        
        if (is_short and is_frequent) or has_repeated:
            potential_slang[word] = count
    
    print(f"\n❓ Potential missing slang: {len(potential_slang)}")
    if potential_slang:
        print("\nTop 100 potential slang (sorted by frequency):")
        print("-" * 80)
        for i, (word, count) in enumerate(sorted(potential_slang.items(), key=lambda x: x[1], reverse=True)[:100], 1):
            # Check if has repeated chars
            has_repeat = bool(re.search(r'(.)\1{2,}', word))
            marker = "🔄" if has_repeat else "  "
            print(f"{i:3}. {marker} '{word}' - appears {count:,} times")
    
    # Also check for emoticons
    print("\n\n🔍 Scanning for text emoticons...")
    emoticon_patterns = [
        r':\)+',      # :), :)), :)))
        r':\(+',      # :(, :((, :(((
        r'=\)+',      # =), =)), =)))
        r':\*+',      # :*, :**
        r'<3+',       # <3, <33
        r'>\.<',      # >.<
        r'\^\^+',     # ^^, ^^^
        r'T_T', r'T\.T',
        r'-_-', r'-\.-',
        r':v', r':V',
        r'=]', r':\]',
        r'xD', r'XD',
        r':p', r':P',
        r';-?\)', r';\)+',
    ]
    
    all_emoticons = []
    for text in df['Sentence']:
        if isinstance(text, str):
            for pattern in emoticon_patterns:
                matches = re.findall(pattern, text)
                all_emoticons.extend(matches)
    
    emoticon_counter = Counter(all_emoticons)
    missing_emoticons = {emo: count for emo, count in emoticon_counter.items() 
                        if emo not in emoji_handler.emoticon_dict}
    
    print(f"\n❓ Missing emoticons: {len(missing_emoticons)}")
    if missing_emoticons:
        print("\nMissing emoticons (sorted by frequency):")
        print("-" * 80)
        for i, (emo, count) in enumerate(sorted(missing_emoticons.items(), key=lambda x: x[1], reverse=True)[:30], 1):
            print(f"{i:3}. '{emo}' - appears {count:,} times")
    
    # Save results
    print("\n\n💾 Saving results...")
    output_dir = project_root / "report"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "missing_tokens_analysis.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("MISSING TOKENS ANALYSIS\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("MISSING EMOJIS\n")
        f.write("-" * 80 + "\n")
        for i, (emoji, count) in enumerate(sorted(missing_emojis.items(), key=lambda x: x[1], reverse=True), 1):
            code_point = f"U+{ord(emoji):04X}"
            f.write(f"{i:3}. {emoji}  ({code_point}) - {count:,} times\n")
        
        f.write("\n\nPOTENTIAL MISSING SLANG\n")
        f.write("-" * 80 + "\n")
        for i, (word, count) in enumerate(sorted(potential_slang.items(), key=lambda x: x[1], reverse=True), 1):
            has_repeat = bool(re.search(r'(.)\1{2,}', word))
            marker = "[REPEAT]" if has_repeat else ""
            f.write(f"{i:3}. '{word}' {marker} - {count:,} times\n")
        
        f.write("\n\nMISSING EMOTICONS\n")
        f.write("-" * 80 + "\n")
        for i, (emo, count) in enumerate(sorted(missing_emoticons.items(), key=lambda x: x[1], reverse=True), 1):
            f.write(f"{i:3}. '{emo}' - {count:,} times\n")
    
    print(f"✅ Saved to: {output_file}")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Missing emojis: {len(missing_emojis)}")
    print(f"Potential missing slang: {len(potential_slang)}")
    print(f"Missing emoticons: {len(missing_emoticons)}")


if __name__ == "__main__":
    csv_path = project_root / "data" / "raw" / "train_merged.csv"
    
    if not csv_path.exists():
        print(f"❌ File not found: {csv_path}")
    else:
        analyze_dataset(csv_path)

