#! /usr/bin/env python
# Copyright 2021 John Hanley. MIT licensed.
# usage:
#   python -m vision.find_shape.find_ngons
import cv2

from .web_image import WebImage

CYAN = (255, 255, 0)  # BGR
PURPLE = (128, 0, 128)
BLACK = (0, 0, 0)


def _find_center(contour):
    x, y = 0, 0
    m = cv2.moments(contour)
    if m['m00'] != 0.0:
        x = int(m['m10'] / m['m00'])
        y = int(m['m01'] / m['m00'])
    return x, y


def find_ngons(web_img, font=cv2.FONT_HERSHEY_SIMPLEX):
    img = cv2.imread(web_img.image())
    blur = cv2.GaussianBlur(img, ksize=(9, 9), sigmaX=30)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours[1:]:  # 1st contour is entire image

        cv2.drawContours(img, [contour], 0, CYAN, thickness=5)

        perimeter = cv2.arcLength(contour, closed=True)
        approx = cv2.approxPolyDP(contour, 0.01 * perimeter, closed=True)
        n_gon = f'{len(approx)}-gon'

        x, y = _find_center(contour)
        cv2.putText(img, n_gon, (x, y), font, fontScale=0.6, color=PURPLE, thickness=2)

    cv2.imshow('shapes', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


urls = [
    'https://i.ytimg.com/vi/Cb2h2-lkJq0/maxresdefault.jpg',
    'http://cdn.ecommercedns.uk/files/8/204798/2/1949692/x-1922-set-of-9-shapes-standard-01.jpg',
    'https://www.oysterenglish.com/images/shapes-vocabulary.jpg',
    'https://nurseryrhymesforbabies.com/wp-content/uploads/2018/03/shapes-learn-kids-school-1461236929n4W.jpg',
    'https://1.bp.blogspot.com/-dp3CzgO2G6g/UEZf__CeUzI/AAAAAAAADE8/IbPWGpNDRJk/s1600/Geo+Rocket.jpg',
    'https://cdn11.bigcommerce.com/s-mgidzs2fr0/products/318/images/1070/basic-shapes__01302.1500356170.500.750.jpg',
    'https://www.purposegames.com/images/games/background/353/353313.png',
    'https://learningmole.com/wp-content/uploads/2020/05/whats-a-polygon-696x676.png',
]

if __name__ == '__main__':
    find_ngons(WebImage(urls[-1]))
