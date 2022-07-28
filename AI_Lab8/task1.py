from PIL import Image
from matplotlib import image
from matplotlib import pyplot


def showImage():
    # load the image
    image = Image.open('f1.jpg')
    # summarize some details about the image
    print(image.format)
    print(image.mode)
    print(image.size)
    # show the image
    image.show()


def convertToNumpyArray():
    # load image as pixel array
    data = image.imread('f1.jpg')
    # summarize shape of the pixel array
    print(data.dtype)
    print(data.shape)
    # display the array of pixels as an image
    pyplot.imshow(data)
    pyplot.show()


def resize():
    # load the image
    image = Image.open('f1.jpg')
    # report the size of the image
    print(image.size)
    # create a thumbnail and preserve aspect ratio
    image.thumbnail((100, 100))
    # report the size of the thumbnail
    print(image.size)


def flip():
    image = Image.open('f1.jpg')
    hoz_flip = image.transpose(Image.FLIP_LEFT_RIGHT)
    ver_flip = image.transpose(Image.FLIP_TOP_BOTTOM)
    pyplot.subplot(311)
    pyplot.imshow(image)
    pyplot.subplot(312)
    pyplot.imshow(hoz_flip)
    pyplot.subplot(313)
    pyplot.imshow(ver_flip)
    pyplot.show()
    pyplot.subplot(321)
    pyplot.imshow(image)
    pyplot.subplot(322)
    pyplot.imshow(image.rotate(45))
    pyplot.subplot(323)
    pyplot.imshow(image.rotate(90))
    pyplot.show()


showImage()
convertToNumpyArray()
resize()
flip()
