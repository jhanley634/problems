#! /usr/bin/env python
# Copyright 2021 John Hanley. MIT licensed.
from os.path import expanduser
from pathlib import Path

import cv2
import requests


class WebImage:

    def __init__(self, url, fname='shapes.jpg', temp=Path('/tmp')):
        self.url = url
        self.fspec = temp / fname

    def image(self):
        if not self.fspec.exists():
            resp = requests.get(self.url)
            resp.raise_for_status()
            with open(self.fspec, 'wb') as fout:
                fout.write(resp.content)
        with open(self.fspec, 'b') as fin:
            return fin.read()


def _find_center(contour):
    x, y = 0, 0
    m = cv2.moments(contour)
    if m['m00'] != 0.0:
        x = int(m['m10'] / m['m00'])
        y = int(m['m01'] / m['m00'])
    return x, y


def find_ngons(infile='shapes.jpg', font=cv2.FONT_HERSHEY_SIMPLEX):
    cyan = (255, 255, 0)  # BGR
    purple = (128, 0, 128)
    img = cv2.imread(expanduser(f'~/Desktop/{infile}'))
    blur = cv2.GaussianBlur(img, ksize=(7, 7), sigmaX=30)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(
        threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours[1:]:  # 1st contour is entire image

        cv2.drawContours(img, [contour], 0, cyan, thickness=5)

        perimeter = cv2.arcLength(contour, closed=True)
        approx = cv2.approxPolyDP(contour, 0.01 * perimeter, closed=True)
        n_gon = f'{len(approx)}-gon'

        x, y = _find_center(contour)
        cv2.putText(img, n_gon, (x, y), font, fontScale=0.6, color=purple, thickness=2)

    cv2.imshow('shapes', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    find_ngons()
