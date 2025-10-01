import streamlit as st
import time
import re
from collections import Counter

# --- Cấu hình Mô hình (Ghi chú) ---
# Trong thực tế, bạn sẽ cần các thư viện như transformers và torch.
# Ví dụ:
# from transformers import AutoModelForSequenceClassification, AutoTokenizer
# MODEL_NAME = "một_mô_hình_phân_loại_tiếng_việt_trên_huggingface"
# @st.cache_resource # Dùng st.cache_resource để tải mô hình chỉ 1 lần
# def load_model():
#     tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
#     model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
#     return tokenizer, model
# tokenizer, model = load_model()

# --- TỪ ĐIỂN TỪ NGỮ ĐỘC HẠI/THÔ TỤC ---
TOXIC_WORDS = {
    "high_severity": [
        "con cặc", "lồn", "cặc", "buồi", "địt", "đụ", "chịch", "cave",
        "đĩ", "đỉ", "loz", "cailon", "cailoz", "duma", "dume", "ditme",
        "dmm", "dcm", "dkm", "dcmm", "dkm", "dkmm", "dkmml", "dkmmln"
    ],
    "medium_severity": [
        "đồ khốn", "đồ ngu", "thằng ngu", "con ngu", "óc chó", "não cá",
        "đần", "ngu ngốc", "ngu xuẩn", "đồ điên", "thằng điên", "con điên"
    ],
    "low_severity": [
        "chết tiệt", "trời đánh", "thánh vật", "đồ tồi", "vô dụng",
        "rác rưởi", "cặn bã", "hạ lưu"
    ]
}

POSITIVE_WORDS = [
    "tuyệt vời", "xuất sắc", "hoàn hảo", "thích thú", "hài lòng", "vui vẻ",
    "hạnh phúc", "tốt đẹp", "ấn tượng", "thú vị", "hào hứng", "phấn khích"
]


# --- Hàm Phân tích Nội dung Nâng cao ---
@st.cache_data
def analyze_content_advanced(text):
    """
    Hàm phân tích nội dung nâng cao với nhận diện từ ngữ độc hại
    """
    if not text:
        return {
            "label": "Chưa có nội dung",
            "color": "warning",
            "details": "Vui lòng nhập văn bản.",
            "severity": 0,
            "toxic_words_found": [],
            "word_count": 0
        }

    # Giả lập thời gian xử lý của mô hình
    time.sleep(1.5)

    text_lower = text.lower()
    word_count = len(text.split())

    # Phát hiện từ ngữ độc hại
    toxic_words_found = []
    severity_score = 0

    for severity_level, words in TOXIC_WORDS.items():
        for word in words:
            if word in text_lower:
                toxic_words_found.append(word)
                if severity_level == "high_severity":
                    severity_score += 3
                elif severity_level == "medium_severity":
                    severity_score += 2
                elif severity_level == "low_severity":
                    severity_score += 1

    # Phát hiện từ tích cực
    positive_words_found = [word for word in POSITIVE_WORDS if word in text_lower]

    # Phân loại dựa trên kết quả phân tích
    if severity_score >= 3:
        return {
            "label": "🚨 NỘI DUNG ĐỘC HẠI NGHIÊM TRỌNG",
            "color": "error",
            "details": f"Phát hiện {len(toxic_words_found)} từ ngữ thô tục/độc hại. Nội dung vi phạm nghiêm trọng nguyên tắc cộng đồng.",
            "severity": severity_score,
            "toxic_words_found": toxic_words_found,
            "positive_words_found": positive_words_found,
            "word_count": word_count,
            "risk_level": "CAO"
        }
    elif severity_score >= 1:
        return {
            "label": "⚠️ NỘI DUNG TIÊU CỰC",
            "color": "warning",
            "details": f"Phát hiện {len(toxic_words_found)} từ ngữ tiêu cực. Cần xem xét lại nội dung.",
            "severity": severity_score,
            "toxic_words_found": toxic_words_found,
            "positive_words_found": positive_words_found,
            "word_count": word_count,
            "risk_level": "TRUNG BÌNH"
        }
    elif positive_words_found:
        return {
            "label": "😄 NỘI DUNG TÍCH CỰC",
            "color": "success",
            "details": f"Phát hiện {len(positive_words_found)} từ ngữ tích cực. Nội dung mang tính xây dựng.",
            "severity": 0,
            "toxic_words_found": [],
            "positive_words_found": positive_words_found,
            "word_count": word_count,
            "risk_level": "THẤP"
        }
    elif word_count > 15:
        return {
            "label": "📚 NỘI DUNG THÔNG TIN",
            "color": "info",
            "details": "Nội dung mang tính chất thông tin, trung lập.",
            "severity": 0,
            "toxic_words_found": [],
            "positive_words_found": [],
            "word_count": word_count,
            "risk_level": "THẤP"
        }
    else:
        return {
            "label": "💬 NỘI DUNG BÌNH THƯỜNG",
            "color": "secondary",
            "details": "Nội dung ngắn, không phát hiện vấn đề.",
            "severity": 0,
            "toxic_words_found": [],
            "positive_words_found": [],
            "word_count": word_count,
            "risk_level": "THẤP"
        }


# --- Cấu hình Trang ---
st.set_page_config(
    page_title="Phân Tích Nội dung Tiếng Việt Nâng Cao",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Sidebar với Thông tin Bổ sung ---
with st.sidebar:
    st.header("📊 Thông tin Phân tích")
    st.markdown("""
    **Mức độ Rủi ro:**
    - 🟢 **THẤP**: Nội dung an toàn
    - 🟡 **TRUNG BÌNH**: Có từ tiêu cực
    - 🔴 **CAO**: Nhiều từ độc hại

    **Phân loại Từ ngữ:**
    - 🔴 Độc hại Nghiêm trọng
    - 🟡 Tiêu cực Nhẹ
    - 🟢 Tích cực
    """)


# --- Main Content ---
st.title("🔍 Phân Tích Nội dung Tiếng Việt Nâng Cao")
st.markdown("Phát hiện và phân loại nội dung độc hại, thô tục và tích cực trong văn bản tiếng Việt.")

# --- Khu vực Nhập liệu ---
col1, col2 = st.columns([2, 1])

with col1:
    with st.container(border=True):
        st.subheader("📝 Nhập Nội dung Cần Phân tích")
        text = st.text_area(
            "Nhập văn bản tiếng Việt:",
            placeholder="Ví dụ: Dịch vụ này thật tệ hại!...",
            height=150,
            label_visibility="collapsed"
        )

        if st.button("🔍 Phân Tích Nội dung", use_container_width=True, type="primary"):
            if not text.strip():
                st.warning("⚠️ Vui lòng nhập nội dung để phân tích.")
            else:
                with st.spinner('🔄 Đang phân tích nội dung, kiểm tra từ ngữ độc hại...'):
                    result = analyze_content_advanced(text)

                # --- Hiển thị Kết quả Chi tiết ---
                st.markdown("---")
                st.subheader("📊 Kết Quả Phân Tích Chi Tiết")

                # Hiển thị kết quả chính
                if result["color"] == "error":
                    st.error(f"**NHÃN PHÂN LOẠI:** {result['label']}")
                elif result["color"] == "warning":
                    st.warning(f"**NHÃN PHÂN LOẠI:** {result['label']}")
                elif result["color"] == "success":
                    st.success(f"**NHÃN PHÂN LOẠI:** {result['label']}")
                elif result["color"] == "info":
                    st.info(f"**NHÃN PHÂN LOẠI:** {result['label']}")
                else:
                    st.write(f"**NHÃN PHÂN LOẠI:** {result['label']}")

                # Thông tin chi tiết
                col_info1, col_info2, col_info3 = st.columns(3)

                with col_info1:
                    st.metric("📝 Số từ", result["word_count"])

                with col_info2:
                    st.metric("⚠️ Từ độc hại", len(result["toxic_words_found"]))

                with col_info3:
                    st.metric("🎯 Mức độ rủi ro", result["risk_level"])

                # Chi tiết từ ngữ phát hiện
                if result["toxic_words_found"]:
                    with st.expander("🔴 **TỪ NGỮ ĐỘC HẠI PHÁT HIỆN**", expanded=True):
                        st.warning("Cảnh báo: Các từ sau bị coi là độc hại/thô tục:")
                        for word in result["toxic_words_found"]:
                            st.write(f"• `{word}`")

                if result["positive_words_found"]:
                    with st.expander("🟢 **TỪ NGỮ TÍCH CỰC PHÁT HIỆN**"):
                        st.success("Các từ tích cực được tìm thấy:")
                        for word in result["positive_words_found"]:
                            st.write(f"• `{word}`")

                # Giải thích chi tiết
                st.info(f"**📋 Giải thích:** {result['details']}")




# --- Footer ---
st.markdown("---")
st.caption("""
**Lưu ý:** Ứng dụng đang sử dụng từ điển từ ngữ để phân loại. 
Trong thực tế, hệ thống sẽ sử dụng mô hình AI để phân tích ngữ cảnh chính xác hơn.
""")

# Khởi tạo session state cho demo text
if 'demo_text' not in st.session_state:
    st.session_state.demo_text = ""