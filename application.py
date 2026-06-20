import streamlit as st
import joblib

# Load model
model = joblib.load("phishing_detector.pkl")

# Page configuration
st.set_page_config(
    page_title="Phishing URL Detector",
    page_icon="🛡️",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
.main {
    padding-top: 2rem;
}

.stTextInput > div > div > input {
    font-size: 18px;
}

.result-box {
    padding: 15px;
    border-radius: 10px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(
    """
    <h1 style='text-align: center; color: #1E88E5;'>
        Phishing URL Detector
    </h1>
    <p style='text-align: center; font-size:18px;'>
        Detect whether a website URL is legitimate or phishing 
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# URL Input
url = st.text_input(
    " Enter Website URL",
    placeholder="https://example.com"
)

# Check Button
if st.button("🚀 Analyze URL", use_container_width=True):

    if not url.strip():
        st.warning("⚠️ Please enter a URL.")
    else:
        try:
            prediction = model.predict([url])[0]
            probability = model.predict_proba([url])[0]

            phishing_conf = round(probability[1] * 100, 2)
            legit_conf = round(probability[0] * 100, 2)

            st.subheader("Analysis Result")

            if prediction == 1:
                st.error("🚨 Phishing Website Detected!")

                st.metric(
                    label="Phishing Probability",
                    value=f"{phishing_conf}%"
                )

                st.progress(int(phishing_conf))

            else:
                st.success("✅ Legitimate Website")

                st.metric(
                    label="Legitimacy Probability",
                    value=f"{legit_conf}%"
                )

                st.progress(int(legit_conf))

            # Detailed probabilities
            st.subheader("Confidence Scores")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "✅ Legitimate",
                    f"{legit_conf}%"
                )

            with col2:
                st.metric(
                    "🚨 Phishing",
                    f"{phishing_conf}%"
                )

        except Exception as e:
            st.error(f"Error: {e}")



    st.divider()

    