import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

def apply_soft_tone(image):
    # Convert to float32
    image_float = np.float32(image) / 255.0
    
    # Increase brightness slightly
    brightness = 1.1
    image_bright = image_float * brightness
    
    # Soft tone curve adjustment
    image_curve = np.power(image_bright, 0.95)
    
    # Adjust saturation
    hsv = cv2.cvtColor(image_curve, cv2.COLOR_RGB2HSV)
    hsv[:, :, 1] = hsv[:, :, 1] * 0.9  # Reduce saturation slightly
    image_sat = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    
    # Add slight warm tone
    warm_filter = np.array([1.1, 1.0, 0.9])
    image_warm = image_sat * warm_filter
    
    # Ensure values are in valid range
    final_image = np.clip(image_warm, 0, 1)
    
    # Convert back to uint8
    return (final_image * 255).astype(np.uint8)

def main():
    st.title('소프트톤 이미지 필터')
    st.write('부드러운 색감으로 이미지를 변환해보세요.')
    
    # Multiple file uploader
    uploaded_files = st.file_uploader(
        "이미지를 선택하세요 (여러 장 선택 가능)",
        type=['jpg', 'jpeg', 'png'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.write(f"### {uploaded_file.name}")
            
            # Read image
            image = Image.open(uploaded_file)
            image = np.array(image)
            
            # Process image
            processed = apply_soft_tone(image)
            
            # Display original and processed images side by side
            col1, col2 = st.columns(2)
            with col1:
                st.write("원본 이미지")
                st.image(image)
            with col2:
                st.write("처리된 이미지")
                st.image(processed)
            
            # Convert processed image to bytes for download
            processed_bytes = io.BytesIO()
            Image.fromarray(processed).save(processed_bytes, format='PNG')
            
            # Create download button for this image
            base_name = uploaded_file.name.rsplit('.', 1)[0]
            st.download_button(
                label=f'{uploaded_file.name} 다운로드',
                data=processed_bytes.getvalue(),
                file_name=f'{base_name}_soft_tone.png',
                mime='image/png',
                key=f'download_{base_name}'  # Unique key for each button
            )
            
            # Add a separator between images
            st.markdown("---")

if __name__ == '__main__':
    main()
