#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/293180/difference-of-gaussian-function
import cv2


def main() -> None:
    # lena = "https://i.sstatic.net/Q3hecnZb.png"
    lena = "/tmp/Q3hecnZb.png"
    img = cv2.imread(lena)
    height, width, depth = img.shape
    assert depth == 3

    k_size = 3
    sigma = 3
    blur = cv2.GaussianBlur(img, ksize=(k_size, k_size), sigmaX=sigma)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_OTSU)
    cv2.imwrite("/tmp/lena.png", thresh)
    cv2.imshow("lena", thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
