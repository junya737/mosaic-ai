import face_recognition
import cv2


def process_images(uploaded_image, known_face_image, mosaic_factor=0.1):
    # Load the images
    unknown_image = face_recognition.load_image_file(uploaded_image)
    known_image = face_recognition.load_image_file(known_face_image)

    # Detect faces
    unknown_face_bboxes = face_recognition.face_locations(unknown_image)
    known_face_encodings = face_recognition.face_encodings(known_image)

    if known_face_encodings:
        known_encoding = known_face_encodings[0]
        unknown_face_encodings = face_recognition.face_encodings(unknown_image, unknown_face_bboxes)
        matches = face_recognition.compare_faces(unknown_face_encodings, known_encoding)

        # Apply mosaic to non-matching faces
        for (top, right, bottom, left), match in zip(unknown_face_bboxes, matches):
            if not match:
                unknown_image = add_mosaic(unknown_image, (top, right, bottom, left), factor=mosaic_factor)

    return unknown_image

def add_mosaic(image, bbox, factor=0.1):
    top, right, bottom, left = bbox
    face = image[top:bottom, left:right]
    h, w = face.shape[:2]
    small = cv2.resize(face, (int(w * factor), int(h * factor)), interpolation=cv2.INTER_LINEAR)
    face_mosaic = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
    image[top:bottom, left:right] = face_mosaic
    return image
