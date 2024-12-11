import streamlit as st
from PIL import Image, ImageEnhance
import io
import numpy as np
import base64  # 추가된 import

def apply_tone_mapping(image):
    # Convert PIL Image to numpy array
    img_array = np.array(image).astype(float) / 255.0
    
    # Separate shadows and highlights
    shadows = 1 - img_array
    highlights = img_array
    
    # Adjust shadows (+5~+10) and highlights (-5~0)
    shadows_strength = 0.08  # +8% for shadows
    highlights_strength = 0.03  # -3% for highlights
    
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
    
    # Enhance brightness (+10~+15)
    enhancer = ImageEnhance.Brightness(image)
    image_bright = enhancer.enhance(1.125)  # +12.5%
    
    # Enhance contrast (+15~+20)
    enhancer = ImageEnhance.Contrast(image_bright)
    image_contrast = enhancer.enhance(1.175)  # +17.5%
    
    # Enhance color/saturation (+10~+15)
    enhancer = ImageEnhance.Color(image_contrast)
    image_color = enhancer.enhance(1.125)  # +12.5%
    
    # Enhance warmth by adjusting color balance (+5~+10 temperature)
    r, g, b = image_color.split()
    r = ImageEnhance.Brightness(r).enhance(1.075)  # +7.5% red
    g = ImageEnhance.Brightness(g).enhance(1.025)  # +2.5% green
    b = ImageEnhance.Brightness(b).enhance(0.95)   # -5% blue
    
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
            try:
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
                    st.write("처리된 이미지 (클릭하여 다운로드)")
                    
                    # Convert processed image to bytes for download
                    img_bytes = io.BytesIO()
                    processed.save(img_bytes, format='PNG')
                    img_bytes = img_bytes.getvalue()
                    
                    # Create clickable image that downloads
                    st.markdown(
                        f'<a href="data:image/png;base64,{base64.b64encode(img_bytes).decode()}" download="{uploaded_file.name.rsplit(".", 1)[0]}_edited.png">'
                        f'<img src="data:image/png;base64,{base64.b64encode(img_bytes).decode()}" width="100%"></a>',
                        unsafe_allow_html=True
                    )
                
                st.markdown("---")
                
            except Exception as e:
                st.error(f"이미지 처리 중 오류가 발생했습니다: {str(e)}")

if __name__ == '__main__':
    main() 
