import cv2
from FaceDetection import FaceDetection
import Rectangles

img = cv2.imread("image.jpg")
h, w, _ = img.shape
img = cv2.resize(img, (w * 5, h * 5))

faceDetection = FaceDetection()
faces = faceDetection.detect(img)
print(faces)
Rectangles.draw(faces, img)
cv2.imshow("image", img)
cv2.waitKey(0)

