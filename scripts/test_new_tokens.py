"""
Test New Tokens
===============
Test các emoji và slang mới được thêm vào.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.preprocessing import EmojiHandler, TextNormalizer, PreprocessingPipeline


def test_new_emojis():
    """Test emoji mới"""
    print("=" * 80)
    print("TEST NEW EMOJIS")
    print("=" * 80)
    
    handler = EmojiHandler()
    
    test_cases = [
        ("Buồn quá 🥲", "khóc"),
        ("Xúc động quá 🥹", "xúc động"),
        ("Chán chường 😑", "chán chường"),
        ("Bất mãn 🙄", "bất mãn"),
        ("Ngớ ngẩn 🤡", "ngớ ngẩn"),
        ("Suy nghĩ 🤔", "suy nghĩ"),
        ("Cười thách thức 😏", "cười thách thức"),
        ("Ngầu 😎", "ngầu"),
        ("Cạn lời 😐", "cạn lời"),
        ("Thèm 🤤", "thèm"),
        ("Nóng 🥵", "nóng"),
        ("Sượng 😬", "sượng"),
        ("Sợ 🥶", "sợ"),
        ("Tức 😤", "tức"),
        ("Ngầu 🗿", "ngầu"),
        ("Choáng váng 🥴", "choáng váng"),
        ("Sốc 😧", "sốc"),
        ("Hoang mang 😕", "hoang mang"),
        ("Bó tay 🤦", "bó tay"),
        ("Cảnh báo 🚩", "cảnh báo"),
    ]
    
    print(f"\nTesting {len(test_cases)} new emojis...\n")
    
    passed = 0
    failed = 0
    
    for text, expected_word in test_cases:
        result = handler.convert(text)
        if expected_word in result:
            print(f"✅ {text:30} → {result}")
            passed += 1
        else:
            print(f"❌ {text:30} → {result} (expected '{expected_word}')")
            failed += 1
    
    print(f"\n{'='*80}")
    print(f"Results: {passed} passed, {failed} failed")
    return failed == 0


def test_new_slang():
    """Test slang mới"""
    print("\n" + "=" * 80)
    print("TEST NEW SLANG")
    print("=" * 80)
    
    normalizer = TextNormalizer()
    
    test_cases = [
        ("per này hay lắm", "người"),
        ("tao thích lắm", "tao"),
        ("mày làm gì vậy", "mày"),
        ("nó nói gì vậy", "nó"),
        ("ta đi thôi", "ta"),
        ("vãi quá", "quá"),
        ("ác thật", "ghê"),
    ]
    
    print(f"\nTesting {len(test_cases)} new slang terms...\n")
    
    passed = 0
    failed = 0
    
    for text, expected_word in test_cases:
        result = normalizer.normalize(text)
        if expected_word in result:
            print(f"✅ {text:30} → {result}")
            passed += 1
        else:
            print(f"❌ {text:30} → {result} (expected '{expected_word}')")
            failed += 1
    
    print(f"\n{'='*80}")
    print(f"Results: {passed} passed, {failed} failed")
    return failed == 0


def test_emoticons():
    """Test emoticons with user changes"""
    print("\n" + "=" * 80)
    print("TEST EMOTICONS")
    print("=" * 80)
    
    handler = EmojiHandler()
    
    test_cases = [
        ("Hay quá :v", "cười xòa cho qua"),
        ("Tốt :V", "cười xòa cho qua"),
        ("Ok :)))", "cười"),
        ("Tuyệt =))))", "cười"),
        ("Buồn :(((", "buồn"),
    ]
    
    print(f"\nTesting emoticons...\n")
    
    for text, expected in test_cases:
        result = handler.convert(text)
        status = "✅" if expected in result else "❌"
        print(f"{status} {text:30} → {result}")


def test_full_pipeline():
    """Test full pipeline với các token mới"""
    print("\n" + "=" * 80)
    print("TEST FULL PIPELINE")
    print("=" * 80)
    
    pipeline = PreprocessingPipeline(
        word_segmentation=True,
        segmentation_method='pyvi',  # Use PyVi since VnCoreNLP not installed
        min_word_count=3
    )
    
    test_cases = [
        "Sp này ok lắm per đó 😍😍 :v",
        "Tao thấy mày ngớ ngẩn 🤡 vãi",
        "Nó nói gì vậy 🤔 mình chán chường 😑",
        "Bó tay 🤦 với ông này luôn",
        "Sốc 😧 quá choáng váng 🥴 hết cả lên",
    ]
    
    print(f"\nTesting full pipeline...\n")
    
    for text in test_cases:
        result = pipeline.preprocess(text)
        print(f"Input:  {text}")
        print(f"Output: {result}")
        print()


def main():
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 25 + "NEW TOKENS TEST" + " " * 38 + "║")
    print("╚" + "═" * 78 + "╝")
    
    emoji_ok = test_new_emojis()
    slang_ok = test_new_slang()
    test_emoticons()
    test_full_pipeline()
    
    print("\n" + "=" * 80)
    if emoji_ok and slang_ok:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️  SOME TESTS FAILED")
    print("=" * 80)
    
    # Statistics
    handler = EmojiHandler()
    normalizer = TextNormalizer()
    
    print("\n📊 DICTIONARY STATISTICS:")
    print(f"   Emoji:     {len(handler.emoji_dict)} emoji")
    print(f"   Emoticon:  {len(handler.emoticon_dict)} patterns")
    print(f"   Slang:     {len(normalizer.slang_dict)} terms")
    print()


if __name__ == "__main__":
    main()

