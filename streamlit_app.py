import streamlit as st
from PIL import Image, ImageEnhance
import io
import numpy as np

def apply_tone_mapping(image):
    # Convert PIL Image to numpy array
    img_array = np.array(image).astype(float) / 255.0
    
    # Separate shadows and highlights
    shadows = 1 - img_array
    highlights = img_array
    
    # Adjust shadows and highlights
    shadows_strength = 0.2
    highlights_strength = 0.2
    
    # Apply adjustments
    result = img_array + (shadows * shadows_strength) - (highlights * highlights_strength)
    
    # Ensure values are in valid range
    result = np.clip(result, 0, 1)
    
    # Convert back to PIL Image
    return Image.fromarray((result * 255).astype(np.uint8))

def apply_soft_tone(image):
    # Convert to PIL Image if it's not already
    if not isinstance(image, Image.Image):
        image = Image.fromarray(image)
    
    # Apply tone mapping first
    image = apply_tone_mapping(image)
    
    # Enhance brightness (1.2로 증가)
    enhancer = ImageEnhance.Brightness(image)
    image_bright = enhancer.enhance(1.2)
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(image_bright)
    image_contrast = enhancer.enhance(0.85)
    
    # Enhance color (채도 0.8로 낮춤)
    enhancer = ImageEnhance.Color(image_contrast)
    image_color = enhancer.enhance(0.8)
    
    # Enhance warmth by adjusting the color balance
    r, g, b = image_color.split()
    r = ImageEnhance.Brightness(r).enhance(1.2)  # 레드 채널 강화
    g = ImageEnhance.Brightness(g).enhance(1.1)  # 그린 채널 약간 강화
    b = ImageEnhance.Brightness(b).enhance(0.85)  # 블루 채널 낮춤
    
    return Image.merge('RGB', (r, g, b))

def main():
    st.title('빈티지 소프트톤 필터')
    st.write('따뜻한 빈티지 색감으로 이미지를 변환해보세요.')
    
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
                file_name=f'{base_name}_vintage_tone.png',
                mime='image/png',
                key=f'download_{base_name}'
            )
            
            st.markdown("---")

if __name__ == '__main__':
    main() 
