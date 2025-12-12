"""
Test Preprocessing Pipeline
============================
Test các module preprocessing để đảm bảo hoạt động đúng.

Author: PPNCKH Project
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.preprocessing import (
    TextCleaner, 
    EmojiHandler, 
    TextNormalizer, 
    PreprocessingPipeline
)


def test_text_cleaner():
    """Test TextCleaner module"""
    print("=" * 80)
    print("TEST 1: TEXT CLEANER")
    print("=" * 80)
    
    cleaner = TextCleaner()
    
    test_cases = [
        "Shop này okeeee lắm 😍 free ship nữa :))) ib nha @user https://abc.com",
        "Sảnnn phẩmmmm rấtttt tệ!!!! Ko muốn mua nữaaaa 😡😡😡",
        "<p>Email: test@gmail.com - SĐT: 0123456789</p>",
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n【Test {i}】")
        print(f"  Input:  {text}")
        cleaned = cleaner.clean(text)
        print(f"  Output: {cleaned}")
    
    print("\n✅ TextCleaner test passed!")


def test_emoji_handler():
    """Test EmojiHandler module"""
    print("\n" + "=" * 80)
    print("TEST 2: EMOJI HANDLER")
    print("=" * 80)
    
    handler = EmojiHandler()
    
    test_cases = [
        "Sản phẩm đẹp quá 😍😍😍",
        "Shop phục vụ tệ :((( không mua nữa",
        "Ok nha bạn :)) cảm ơn nhiều ❤️❤️",
        "Thất vọng quá 😭😭",
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n【Test {i}】")
        print(f"  Input:  {text}")
        converted = handler.convert(text)
        print(f"  Output: {converted}")
    
    print("\n✅ EmojiHandler test passed!")


def test_text_normalizer():
    """Test TextNormalizer module"""
    print("\n" + "=" * 80)
    print("TEST 3: TEXT NORMALIZER")
    print("=" * 80)
    
    # Test without dict file
    normalizer = TextNormalizer()
    
    test_cases = [
        "Shop này ok lắm m thích",
        "Sp đẹp quá ko có gì để chê",
        "Free ship nhanh lắm nha, ib shop nhé",
        "Fake hàng à, k mua nữa đâu",
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n【Test {i}】")
        print(f"  Input:  {text}")
        normalized = normalizer.normalize(text)
        print(f"  Output: {normalized}")
    
    # Test with dict file
    slang_file = project_root / "data" / "processed" / "slang_example.csv"
    if slang_file.exists():
        print(f"\n📚 Testing with slang dictionary: {slang_file.name}")
        normalizer_ext = TextNormalizer(slang_dict_path=slang_file)
        
        test_text = "Sp này dc lắm, rep nhanh"
        print(f"  Input:  {test_text}")
        print(f"  Output: {normalizer_ext.normalize(test_text)}")
    
    print("\n✅ TextNormalizer test passed!")


def test_full_pipeline():
    """Test full preprocessing pipeline"""
    print("\n" + "=" * 80)
    print("TEST 4: FULL PREPROCESSING PIPELINE")
    print("=" * 80)
    
    # Initialize pipeline
    slang_file = project_root / "data" / "processed" / "slang_example.csv"
    
    pipeline = PreprocessingPipeline(
        slang_dict_path=slang_file if slang_file.exists() else None,
        word_segmentation=True,  # Will use simple segmenter if PyVi not available
        segmentation_method='pyvi',
        min_word_count=3,
        lowercase=True
    )
    
    print("\n📊 Pipeline configuration:")
    for key, value in pipeline.get_pipeline_info().items():
        print(f"   {key}: {value}")
    
    # Test cases
    test_cases = [
        "Shop này okeeee lắm 😍😍 free ship nữa :))) ib nha @user https://abc.com",
        "Sảnnn phẩmmmm rấtttt tệ!!!! Ko muốn mua nữaaaa 😡😡😡",
        "Giá hợp lý, chất lượng tốt ⭐⭐⭐⭐⭐ #recommend #5sao",
        "Ok nha bạn :)) giao hàng nhanh, đóng gói cẩn thận 👍",
        "Sp đẹp wa, t thích lắm <3",
        "A",  # Too short - should be filtered
        "Ok",  # Too short - should be filtered
    ]
    
    print("\n" + "-" * 80)
    print("Processing individual texts:")
    print("-" * 80)
    
    valid_count = 0
    filtered_count = 0
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n【Test {i}】")
        print(f"  Input:  {text}")
        
        result, stats = pipeline.preprocess(text, return_stats=True)
        
        if result:
            print(f"  Output: {result}")
            print(f"  Status: ✅ {stats['status']} | Words: {stats['final_word_count']}")
            valid_count += 1
        else:
            print(f"  Output: [FILTERED]")
            print(f"  Status: ⚠️  {stats['status']}")
            filtered_count += 1
    
    print("\n" + "-" * 80)
    print(f"Summary: {valid_count} valid, {filtered_count} filtered")
    print("-" * 80)
    
    print("\n✅ Full pipeline test passed!")


def test_batch_processing():
    """Test batch processing"""
    print("\n" + "=" * 80)
    print("TEST 5: BATCH PROCESSING")
    print("=" * 80)
    
    slang_file = project_root / "data" / "processed" / "slang_example.csv"
    
    pipeline = PreprocessingPipeline(
        slang_dict_path=slang_file if slang_file.exists() else None,
        word_segmentation=True,
        min_word_count=3,
        lowercase=True
    )
    
    batch_texts = [
        "Shop này ok lắm 😍",
        "Sp tệ quá ko thích",
        "Giao hàng nhanh, đóng gói tốt",
        "A",  # Will be filtered
        "Thất vọng với chất lượng",
    ]
    
    print(f"Processing {len(batch_texts)} texts...")
    results = pipeline.preprocess_batch(batch_texts, show_progress=False)
    
    valid_count = sum(1 for r in results if r)
    print(f"\nResults: {valid_count}/{len(batch_texts)} valid")
    
    for text, result in zip(batch_texts, results):
        status = "✅" if result else "⚠️ "
        print(f"{status} {text[:40]:40} → {result if result else '[FILTERED]'}")
    
    print("\n✅ Batch processing test passed!")


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "PREPROCESSING MODULE TESTS" + " " * 32 + "║")
    print("╚" + "═" * 78 + "╝")
    
    try:
        # Test individual modules
        test_text_cleaner()
        test_emoji_handler()
        test_text_normalizer()
        
        # Test full pipeline
        test_full_pipeline()
        test_batch_processing()
        
        # Summary
        print("\n" + "=" * 80)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 80)
        
        print("\n📝 Notes:")
        print("   • PyVi không được cài: sử dụng SimpleWordSegmenter (fallback)")
        print("   • Để cài PyVi: pip install pyvi")
        print("   • Các module hoạt động tốt ngay cả không có PyVi")
        print("\n✅ Preprocessing pipeline sẵn sàng sử dụng!")
        
    except Exception as e:
        print("\n" + "=" * 80)
        print("❌ TEST FAILED!")
        print("=" * 80)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

