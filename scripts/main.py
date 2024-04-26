import face_recognition
import cv2


def add_mosaic(image, bbox, factor=0.1):
    image = image.copy()  # Create a copy of the image
    top, right, bottom, left = bbox
    face = image[top:bottom, left:right]
    h, w = face.shape[:2]
    small = cv2.resize(
        face, (int(w * factor), int(h * factor)), 
        interpolation=cv2.INTER_LINEAR
    )
    face_mosaic = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
    image[top:bottom, left:right] = face_mosaic
    return image


unknown_image_path = "../data/raw/faces.jpeg"
known_image_path = "../data/raw/asian_guy.jpeg"
save_path = "../data/result/mosaic_faces.jpeg"

# Load an image
image = face_recognition.load_image_file(unknown_image_path)
# Detect face locations
face_bboxes = face_recognition.face_locations(image)

# Extract faces
faces = []
for bbox in face_bboxes:
    top, right, bottom, left = bbox
    face = image[top:bottom, left:right]
    faces.append(face)

# Extract face encodings
face_encodings = []
for face in faces:
    face_encoding = face_recognition.face_encodings(cv2.resize(face,
                                                               (256, 256)))[0]
    face_encodings.append(face_encoding)

# Load a known image
known_image = face_recognition.load_image_file(known_image_path)
known_encoding = face_recognition.face_encodings(known_image)[0]

# Compare face encodings
results = []
for i, face_encoding in enumerate(face_encodings):
    results.append(face_recognition.compare_faces([known_encoding],
                                                  face_encoding)[0])

# Remove faces that are similar to the known face
"TODO: It shouldn't be break statement."
for i, result in enumerate(results):
    if result:
        face_bboxes.pop(i)
        break

# Add mosaic to the faces
mosaic_image = image.copy()
for bbox in face_bboxes:
    mosaic_image = add_mosaic(mosaic_image, bbox, factor=0.15)

# Save the image
cv2.imwrite(save_path, cv2.cvtColor(mosaic_image, cv2.COLOR_RGB2BGR))
