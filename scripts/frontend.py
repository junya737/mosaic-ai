import streamlit as st
from PIL import Image
import io
from backend import process_images

st.title('あなた以外をモザイク処理するAI')
st.write('SNSに写真をアップするとき，他の人の顔をモザイク処理したいけど，自分の顔は見せたい．そんなときありませんか？')
st.write('AIの力を使って，画像の中からあなたの顔を認識し，あなた以外の顔をモザイク処理します．')


mosaic_factor = st.slider("モザイクの大きさを調整してください．小さいほうが粗いモザイクです．", 0.01, 1.0, 0.1)

uploaded_image = st.file_uploader("モザイク処理したい画像を選択してください．", type=['jpg', 'png', 'jpeg'])
if uploaded_image:
    uploaded_image_pil = Image.open(uploaded_image)
    st.image(uploaded_image_pil, caption='モザイク処理したい画像', width=300)

known_face_image = st.file_uploader("あなたの画像をアップロードしてください．", type=['jpg', 'png', 'jpeg'])

if known_face_image:
    known_face_image_pil = Image.open(known_face_image)
    st.image(known_face_image_pil, caption='あなたの画像', width=300)


if st.button('実行！'):
    if uploaded_image and known_face_image:
        
        # Process the images
        processed_image = process_images(uploaded_image, known_face_image,
                                        mosaic_factor=mosaic_factor)

        # Display and allow download of the final image
        final_image = Image.fromarray(processed_image)
        st.image(final_image, caption='モザイク処理された画像', use_column_width=True)

        # Convert to bytes and let user download it
        buf = io.BytesIO()
        final_image.save(buf, format='JPEG')
        byte_im = buf.getvalue()
        st.download_button(
            label="画像をダウンロード",
            data=byte_im,
            file_name="mosaic_face.jpg",
            mime="image/jpeg"
        )
