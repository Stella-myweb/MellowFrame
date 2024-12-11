import streamlit as st
from PIL import Image, ImageEnhance
import io
import numpy as np

def apply_filter(image, filter_strength):
    # Convert PIL Image to numpy array
    img_array = np.array(image).astype(float) / 255
    
    # Basic tone mapping
    shadows = 1 - img_array
    result = img_array + (shadows * filter_strength * 0.5)
    result = np.clip(result, 0, 1)
    
    # Convert back to PIL Image
    processed = Image.fromarray((result * 255).astype(np.uint8))
    
    # Adjust color
    enhancer = ImageEnhance.Color(processed)
    processed = enhancer.enhance(0.9)  # Slightly reduce saturation
    
    # Add warm tone
    r, g, b = processed.split()
    r = ImageEnhance.Brightness(r).enhance(1.1)  # Increase red
    b = ImageEnhance.Brightness(b).enhance(0.9)  # Decrease blue
    
    return Image.merge('RGB', (r, g, b))

def main():
    st.title('소프트톤 이미지 필터')
    
    # 파일 업로더
    uploaded_files = st.file_uploader(
        "이미지를 선택하세요 (여러 장 선택 가능)",
        type=['jpg', 'jpeg', 'png'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        # 필터 강도 슬라이더
        filter_strength = st.slider('필터 강도', 0.0, 1.0, 0.5, 0.1)
        
        processed_images = []
        
        # 모든 이미지 처리 및 표시
        for uploaded_file in uploaded_files:
            # 이미지 읽기
            image = Image.open(uploaded_file).convert('RGB')
            
            # 필터 적용
            processed = apply_filter(image, filter_strength)
            
            # 결과 저장
            processed_images.append({
                'name': uploaded_file.name,
                'processed': processed
            })
            
            # 원본과 처리된 이미지 표시
            col1, col2 = st.columns(2)
            with col1:
                st.write("원본")
                st.image(image, use_column_width=True)
            with col2:
                st.write("처리 결과")
                st.image(processed, use_column_width=True)
            
            st.markdown("---")
        
        # 모든 이미지 다운로드 버튼들을 한 곳에 모음
        st.subheader("처리된 이미지 다운로드")
        for img_data in processed_images:
            # 이미지를 바이트로 변환
            img_byte_arr = io.BytesIO()
            img_data['processed'].save(img_byte_arr, format='PNG')
            
            # 다운로드 버튼 생성
            base_name = img_data['name'].rsplit('.', 1)[0]
            st.download_button(
                label=f'{img_data["name"]} 다운로드',
                data=img_byte_arr.getvalue(),
                file_name=f'{base_name}_soft_tone.png',
                mime='image/png',
                key=f'download_{base_name}'
            )

if __name__ == '__main__':
    main() 
