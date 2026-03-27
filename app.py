import streamlit as st
from openai import OpenAI
import base64

# --- 1. CONFIGURATION ---
# We use st.secrets so your API key stays hidden from the public on GitHub
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI Image Analyzer", layout="centered")
st.title("📸 Image to Text Converter")
st.write("Upload an image and the AI will describe it for you.")

# --- 2. UPLOAD SECTION ---
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Show the user the image they uploaded
    st.image(uploaded_file, caption="Target Image", use_container_width=True)
    
    # Process the image into a format the API understands (Base64)
    bytes_data = uploaded_file.getvalue()
    base64_image = base64.b64encode(bytes_data).decode('utf-8')

    # --- 3. EXECUTION BUTTON ---
    if st.button("Analyze Image"):
        with st.spinner('AI is looking at the image...'):
            try:
                # Call the GPT-4o model (it sees images)
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "Describe this image in detail for a technical report."},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                                },
                            ],
                        }
                    ],
                    max_tokens=500,
                )

                # Show the result to the user
                st.subheader("AI Description:")
                st.info(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Error: {e}")
