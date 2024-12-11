import streamlit as st
from PIL import Image, ImageEnhance
import io

def apply_soft_tone(image):
    # Convert to PIL Image if it's not already
    if not isinstance(image, Image.Image):
        image = Image.fromarray(image)
    
    # Enhance brightness
    enhancer = ImageEnhance.Brightness(image)
    image_bright = enhancer.enhance(1.1)
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(image_bright)
    image_contrast = enhancer.enhance(0.95)
    
    # Enhance color
    enhancer = ImageEnhance.Color(image_contrast)
    image_color = enhancer.enhance(0.9)
    
    # Enhance warmth by adjusting the color balance
    r, g, b = image_color.split()
    r = ImageEnhance.Brightness(r).enhance(1.1)  # Increase red
    b = ImageEnhance.Brightness(b).enhance(0.9)  # Decrease blue
    image_warm = Image.merge('RGB', (r, g, b))
    
    return image_warm

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
            image = Image.open(uploaded_file).convert('RGB')
            
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
            processed.save(processed_bytes, format='PNG')
            
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
