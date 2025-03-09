import streamlit as st
import base64
import json
import logging
import os
from PIL import Image
import io
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_image(image_base64, few_shot_messages, prompt):
    try:
        # Create messages array for OpenAI
        messages = [
            {"role": "system", "content": "You are an expert at analyzing images for quality control purposes. Provide detailed observations about any defects, damages, or quality issues."}
        ]

        # Add few-shot examples if available
        if few_shot_messages:
            messages.extend(few_shot_messages)
        
        # Add the image to analyze and the prompt
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        })

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",  # GPT-4o has vision capabilities
            messages=messages,
            max_tokens=1000
        )
        
        # Extract response text
        return response.choices[0].message.content
    
    except Exception as e:
        logger.error(f"Error analyzing image: {e}")
        return f"An error occurred during image analysis: {str(e)}"

def main():
    few_shot_messages = []
    
    st.title("Quality Control Image Analysis")
    st.subheader("Quality Control Instructions")
    
    default_prompt = "You have been provided examples images of boxes on a conveyer belt. Identify any similarities or differences compared to the good and bad images, and provide a brief description if the box is damaged or not"
    prompt = st.text_area("How would you like your images analyzed?:", value=default_prompt, height=150)

    # Model selection
    model_options = ["gpt-4o", "gpt-4-vision-preview"]
    selected_model = st.selectbox("Select OpenAI model", model_options)

    # Main columns for the interface
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Reference Good Images")
        num_good_images = st.number_input("Number of Good Images (Optional)", min_value=0, max_value=5, value=0, step=1)
        
        good_images = []
        for i in range(num_good_images):
            good_image = st.file_uploader(f"Good Image {i+1}", type=["jpg", "jpeg", "png"], key=f"good_{i}")
            if good_image is not None:
                good_image_base64 = base64.b64encode(good_image.read()).decode('utf-8')
                good_image_comment = st.text_input(f"Comment for Good Image {i+1}", key=f"good_comment_{i}")
                
                # Display the good image
                img = Image.open(io.BytesIO(base64.b64decode(good_image_base64)))
                st.image(img, caption=f'Good Image {i+1}', use_column_width=True)
                
                if good_image_comment:
                    # Add to few shot examples
                    few_shot_messages.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{good_image_base64}"
                                }
                            }
                        ]
                    })
                    few_shot_messages.append({
                        "role": "assistant",
                        "content": good_image_comment
                    })
                    
                    good_images.append((good_image_base64, good_image_comment))

    with col2:
        st.subheader("Reference Bad Images")
        num_bad_images = st.number_input("Number of Bad Images (Optional)", min_value=0, max_value=5, value=0, step=1)
        
        bad_images = []
        for i in range(num_bad_images):
            bad_image = st.file_uploader(f"Bad Image {i+1}", type=["jpg", "jpeg", "png"], key=f"bad_{i}")
            if bad_image is not None:
                bad_image_base64 = base64.b64encode(bad_image.read()).decode('utf-8')
                bad_image_comment = st.text_input(f"Comment for Bad Image {i+1}", key=f"bad_comment_{i}")
                
                # Display the bad image
                img = Image.open(io.BytesIO(base64.b64decode(bad_image_base64)))
                st.image(img, caption=f'Bad Image {i+1}', use_column_width=True)
                
                if bad_image_comment:
                    # Add to few shot examples
                    few_shot_messages.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{bad_image_base64}"
                                }
                            }
                        ]
                    })
                    few_shot_messages.append({
                        "role": "assistant",
                        "content": bad_image_comment
                    })
                    
                    bad_images.append((bad_image_base64, bad_image_comment))
    
    st.subheader("Image to Analyze")
    uploaded_file = st.file_uploader("Choose an image to analyze", type=["jpg", "jpeg", "png"], key="analyze_image")

    if uploaded_file is not None:
        image_base64 = base64.b64encode(uploaded_file.read()).decode('utf-8')
        
        # Display the uploaded image
        img = Image.open(io.BytesIO(base64.b64decode(image_base64)))
        st.image(img, caption='Image to Analyze', use_column_width=True)

        if st.button("Analyze Image"):
            with st.spinner("Analyzing image..."):
                result = analyze_image(image_base64, few_shot_messages, prompt)
                
                st.markdown("### Analysis Results")
                st.markdown(result)
                
                # Add option to save results
                if st.button("Save Results"):
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"analysis_result_{timestamp}.txt"
                    
                    with open(filename, "w") as f:
                        f.write(result)
                    
                    st.success(f"Results saved to {filename}")

    # Display a folder browser for local images
    st.subheader("Browse Local Images")
    folder_path = st.text_input("Path to image folder (e.g., quality-control-images\Random)", value="quality-control-images\Random")
    
    if os.path.exists(folder_path):
        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if image_files:
            selected_file = st.selectbox("Select an image from folder", image_files)
            
            if selected_file:
                file_path = os.path.join(folder_path, selected_file)
                
                with open(file_path, "rb") as img_file:
                    local_image_bytes = img_file.read()
                    local_image_base64 = base64.b64encode(local_image_bytes).decode('utf-8')
                
                # Display the local image
                local_img = Image.open(io.BytesIO(local_image_bytes))
                st.image(local_img, caption=f'Selected Image: {selected_file}', use_column_width=True)
                
                if st.button("Analyze Local Image"):
                    with st.spinner("Analyzing local image..."):
                        local_result = analyze_image(local_image_base64, few_shot_messages, prompt)
                        
                        st.markdown("### Analysis Results (Local Image)")
                        st.markdown(local_result)
        else:
            st.warning(f"No image files found in {folder_path}")
    else:
        if folder_path:
            st.error(f"Folder not found: {folder_path}")

if __name__ == "__main__":
    try:
        from datetime import datetime
        main()
    except Exception as e:
        logger.error(f"Error running the application: {e}")
        st.error(f"An error occurred: {str(e)}")