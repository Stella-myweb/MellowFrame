import streamlit as st
from PIL import Image, ImageEnhance
import io
import numpy as np

def tone_mapping(image, shadows, highlights, balance):
    # Convert PIL Image to numpy array for tone mapping
    img_array = np.array(image).astype(float) / 255
    
    # Separate shadows and highlights
    shadows_mask = 1 - img_array
    highlights_mask = img_array
    
    # Apply adjustments
    shadows_adjusted = img_array + (shadows_mask * shadows)
    highlights_adjusted = img_array - (highlights_mask * highlights)
    
    # Blend shadows and highlights based on balance
    result = shadows_adjusted * balance + highlights_adjusted * (1 - balance)
    
    # Ensure values are in valid range
    result = np.clip(result, 0, 1)
    
    # Convert back to PIL Image
    return Image.fromarray((result * 255).astype(np.uint8))

def apply_soft_tone(image, brightness, contrast, saturation, warmth, shadows, highlights, balance):
    if not isinstance(image, Image.Image):
        image = Image.fromarray(image)
    
    # Convert to RGB if not already
    image = image.convert('RGB')
    
    # Apply tone mapping
    image = tone_mapping(image, shadows, highlights, balance)
    
    # Enhance brightness
    enhancer = ImageEnhance.Brightness(image)
    image_bright = enhancer.enhance(brightness)
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(image_bright)
    image_contrast = enhancer.enhance(contrast)
    
    # Enhance color
    enhancer = ImageEnhance.Color(image_contrast)
    image_color = enhancer.enhance(saturation)
    
    # Enhance warmth by adjusting color balance
    r, g, b = image_color.split()
    r = ImageEnhance.Brightness(r).enhance(1 + (warmth * 0.2))  # Increase red
    b = ImageEnhance.Brightness(b).enhance(1 - (warmth * 0.1))  # Decrease blue
    return Image.merge('RGB', (r, g, b))

def main():
    st.title('소프트톤 이미지 필터')
    st.write('이미지의 색감과 톤을 조절해보세요.')
    
    # Control panel
    st.sidebar.header('필터 설정')
    brightness = st.sidebar.slider('밝기', 0.5, 1.5, 1.1, 0.1)
    contrast = st.sidebar.slider('대비', 0.5, 1.5, 0.95, 0.1)
    saturation = st.sidebar.slider('채도', 0.5, 1.5, 0.9, 0.1)
    warmth = st.sidebar.slider('따뜻한 톤', 0.0, 1.0, 0.5, 0.1)
    
    st.sidebar.header('톤 매핑 설정')
    shadows = st.sidebar.slider('어두운 부분 밝기', 0.0, 0.5, 0.2, 0.05)
    highlights = st.sidebar.slider('밝은 부분 어둡기', 0.0, 0.5, 0.2, 0.05)
    balance = st.sidebar.slider('밸런스', 0.0, 1.0, 0.5, 0.1)
    
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
            
            # Process image with current settings
            processed = apply_soft_tone(
                image, 
                brightness, 
                contrast, 
                saturation, 
                warmth,
                shadows,
                highlights,
                balance
            )
            
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
                key=f'download_{base_name}'
            )
            
            st.markdown("---")

if __name__ == '__main__':
    main()
