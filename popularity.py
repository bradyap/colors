import numpy as np
from PIL import Image
import timeit


class Color:
    def __init__(self, r, g, b):
        self.r = round(r)
        self.g = round(g)
        self.b = round(b)
        self.count = 1

    def getRgb(self):
        return (self.r, self.g, self.b)

    def proximity(self, other):
        r, g, b = other.getRgb()
        return abs(self.r - r) + abs(self.g - g) + abs(self.b - b)

    def combine(self, other):
        self.count += 1

        r, g, b = other.getRgb()
        self.r = (r + self.r * (self.count - 1)) / self.count
        self.g = (g + self.g * (self.count - 1)) / self.count
        self.b = (b + self.b * (self.count - 1)) / self.count


def showColors(colors):
    images = []
    stops = []

    for c in colors:
        r, g, b = c.getRgb()
        r = round(r)
        g = round(g)
        b = round(b)
        rgb = (r, g, b)
        image = Image.new('RGB', (50, 50), rgb)
        images.append(image)
    for i in range(100, 0, -1):
        if len(images) >= i ** 2 and len(images) % i == 0:
            height = i * 50
            width = int(len(images) / i) * 50
            for j in range(1, i):
                stops.append(int(len(images) / i * j))
            break

    output = Image.new('RGB', (width, height))
    xOffset = 0
    yOffset = 0
    index = 0
    for image in images:
        for stop in stops:
            if index == stop:
                yOffset += 50
                xOffset = 0
        output.paste(image, (xOffset, yOffset))
        xOffset += image.size[0]
        index += 1
    output.show()


def main():
    sensitivity = 70
    compression = 0.1

    print("Finding popular colors with sensitivity of " + str(sensitivity) + " and image compression factor of " + str(compression) + "...")
    im = Image.open('./tests/cat.jpg')
    ow, oh = im.size
    w = int(ow * compression)
    h = int(oh * compression)
    im = im.resize((w, h))
    print("Compressed image from " + str(ow) + "x" + str(oh) + " to " + str(w) + "x" + str(h) + ".")
    im.convert('RGB')

    pixels = np.array(im)
    pixels = pixels.reshape((w, h, 3))
    colors = []

    print("Processing image...")
    start = timeit.default_timer()
    for y in range(h):
        for x in range(w):
            color = Color(pixels[x][y][0], pixels[x][y][1], pixels[x][y][2])
            low = sensitivity
            temp = None

            for c in colors:
                prox = c.proximity(color)

                if prox < low:
                    low = prox
                    temp = c

            if temp is not None:
                temp.combine(color)
            else:
                colors.append(color)
    stop = timeit.default_timer()
    print("Identified " + str(len(colors)) + " colors in " + str(stop - start) + "s.")
    showColors(colors)

if __name__ == '__main__':
    main()
