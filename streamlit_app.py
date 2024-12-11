import streamlit as st
from PIL import Image
from PIL import ImageEnhance
import io
import base64
import numpy as np

def apply_filter(image, filter_strength):
    try:
        # Convert to RGB if not already
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        # Convert to numpy array
        img_array = np.array(image).astype(float) / 255
        
        # Apply soft tone effect
        shadows = 1 - img_array
        result = img_array + (shadows * filter_strength * 0.5)
        result = np.clip(result, 0, 1)
        
        # Convert back to PIL Image
        processed = Image.fromarray((result * 255).astype(np.uint8))
        
        # Color adjustments
        enhancer = ImageEnhance.Color(processed)
        processed = enhancer.enhance(0.9)
        
        # Warm tone
        r, g, b = processed.split()
        r = ImageEnhance.Brightness(r).enhance(1.1)
        b = ImageEnhance.Brightness(b).enhance(0.9)
        
        return Image.merge('RGB', (r, g, b))
    except Exception as e:
        st.error(f"이미지 처리 중 오류가 발생했습니다: {str(e)}")
        return None

def get_image_download_link(img, filename):
    buffered = io.BytesIO()
    img.save(buffered, format='PNG')
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{img_str}" download="{filename}" style="display:block; cursor:pointer;"><img src="data:image/png;base64,{img_str}" style="width:100%;"></a>'
    return href

def main():
    st.title('소프트톤 이미지 필터')
    st.write('이미지를 선택하고 필터 강도를 조절해보세요.')
    
    # 필터 강도 슬라이더
    filter_strength = st.slider('필터 강도', 0.0, 1.0, 0.5, 0.1)
    
    # 파일 업로더
    uploaded_files = st.file_uploader(
        "이미지를 선택하세요 (여러 장 선택 가능)",
        type=['jpg', 'jpeg', 'png'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                # 이미지 읽기
                image = Image.open(uploaded_file)
                
                # 필터 적용
                processed = apply_filter(image, filter_strength)
                
                if processed:
                    # 원본과 처리된 이미지 표시
                    cols = st.columns(2)
                    with cols[0]:
                        st.write("원본")
                        st.image(image, use_column_width=True)
                    
                    with cols[1]:
                        st.write("처리된 이미지 (클릭하여 다운로드)")
                        base_name = uploaded_file.name.rsplit('.', 1)[0]
                        download_filename = f'{base_name}_soft_tone.png'
                        st.markdown(
                            get_image_download_link(processed, download_filename),
                            unsafe_allow_html=True
                        )
                    
                    st.markdown("---")
                    
            except Exception as e:
                st.error(f"{uploaded_file.name} 처리 중 오류가 발생했습니다: {str(e)}")
                continue

if __name__ == '__main__':
    main() 
