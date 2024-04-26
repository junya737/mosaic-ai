import streamlit as st
import face_recognition
import cv2
from PIL import Image
import io

def add_mosaic(image, bbox, factor=0.1):
    top, right, bottom, left = bbox
    face = image[top:bottom, left:right]
    h, w = face.shape[:2]
    small = cv2.resize(face, (int(w * factor), int(h * factor)), interpolation=cv2.INTER_LINEAR)
    face_mosaic = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
    image[top:bottom, left:right] = face_mosaic
    return image


st.title('Privacy Face Mosaic App')
st.write('このアプリでは、指定した人物以外の顔にモザイクをかけます。')

uploaded_image = st.file_uploader("アップロードする画像を選択してください。", type=['jpg', 'png', 'jpeg'])
known_face_image = st.file_uploader("認識させたい人物の画像をアップロードしてください。", type=['jpg', 'png', 'jpeg'])

if uploaded_image and known_face_image:
    # Load the images
    unknown_image = face_recognition.load_image_file(uploaded_image)
    known_image = face_recognition.load_image_file(known_face_image)

    # Detect faces in both images
    unknown_face_bboxes = face_recognition.face_locations(unknown_image)
    known_face_encodings = face_recognition.face_encodings(known_image)

    if known_face_encodings:
        known_encoding = known_face_encodings[0]

        # Find faces in the unknown image
        unknown_face_encodings = face_recognition.face_encodings(unknown_image, unknown_face_bboxes)
        
        # Determine which faces are the same as the known face
        matches = face_recognition.compare_faces(unknown_face_encodings, known_encoding)
        
        # Apply mosaic to non-matching faces
        for (top, right, bottom, left), match in zip(unknown_face_bboxes, matches):
            if not match:
                unknown_image = add_mosaic(unknown_image, (top, right, bottom, left), factor=0.1)

        # Convert the image to display it
        final_image = Image.fromarray(unknown_image)
        st.image(final_image, caption='モザイクが適用された画像', use_column_width=True)

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
