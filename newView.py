from __future__ import division
import pygame, sys
from pygame.locals import *
from PIL import Image
#from numpy import *
import os

#must be divisable by (LCD_HEIGHT/10)
LCD_WIDTH = 1280
#height must be divisable by 10
LCD_HEIGHT = 800
IMAGE_DIR = '../image'

###################################################################
def scaleImage(im):
    "Returns a LCD_WIDTH x LCD_HEIGHT landscape, cropping an axis if necessary, or a any_width x LCD_HEIGHT portrait"
    width, height = im.size
    if (width == LCD_WIDTH) and (height == LCD_HEIGHT):
        return im
    if width > height:  #landscape
        if width > LCD_WIDTH:  #scale down
            ratio = width / LCD_WIDTH
            new_height = height / ratio
            #resize width, if height is > LCD_HEIGHT, resize to width and crop excess height from top and bottom
            if int(new_height) > LCD_HEIGHT:
                new_image = im.resize((LCD_WIDTH, int(new_height)), Image.ANTIALIAS)
                increment = (new_height - LCD_HEIGHT) / 2
                box = (0, int(increment), LCD_WIDTH, int(LCD_HEIGHT + increment))
                new_image = new_image.crop(box)
            #resize width, if height < LCD_HEIGHT resize to height of 800 and crop excess from width
            elif int(new_height) < LCD_HEIGHT:
                ratio = LCD_HEIGHT / height
                new_width = width * ratio
                new_image = im.resize((int(new_width), LCD_HEIGHT), Image.ANTIALIAS)
                increment = (new_width - LCD_WIDTH) / 2
                box = (int(increment), 0, int(LCD_WIDTH + increment), LCD_HEIGHT)
                new_image = new_image.crop(box)
            #if perfect resize
            elif int(new_height) == LCD_HEIGHT:
                new_image = im.resize((LCD_WIDTH, int(new_height)), Image.ANTIALIAS)
                return new_image
        else:  #scale up
            ratio = LCD_WIDTH / width
            new_height = height * ratio
            if new_height > LCD_HEIGHT:
                new_image = im.resize((LCD_WIDTH, int(new_height)), Image.ANTIALIAS)
                increment = (new_height - LCD_HEIGHT) / 2
                box = (0, int(increment), LCD_WIDTH, int(LCD_HEIGHT + increment))
                new_image = new_image.crop(box)
            if new_height < LCD_HEIGHT:
                ratio = LCD_HEIGHT / height
                new_width = width * ratio
                new_image = im.resize((int(new_width), LCD_HEIGHT), Image.ANTIALIAS)
                increment = (new_width - LCD_WIDTH) / 2
                box = (int(increment), 0, int(LCD_WIDTH + increment), LCD_HEIGHT)
                new_image = new_image.crop(box)
    else:  #portrait
        if height > LCD_HEIGHT:  #scale down
            ratio = height / LCD_HEIGHT
            new_width = width / ratio
            new_image = im.resize((int(new_width), LCD_HEIGHT), Image.ANTIALIAS)
        else:  #scale up
            ratio = LCD_HEIGHT / height
            new_width = width * ratio
            new_image = im.resize((int(new_width), LCD_HEIGHT), Image.ANTIALIAS)
    return new_image

###################################################################

def get_imlist(path):
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]

###################################################################################################33
pygame.init()
# pygame.display.set_mode((1280,800))
image_list = get_imlist(IMAGE_DIR)
for im in image_list:
    try:
        next_image = Image.open(im)
    except IOError:
        continue
    new_image = scaleImage(next_image)
    new_image.save(im)

screen = pygame.display.set_mode([LCD_WIDTH, LCD_HEIGHT])
screen.blit(pygame.image.load(image_list[0]).convert(), (0,0))
pygame.display.update()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    for i in range (1,len(image_list)):
        # try:im
        #     next_image = Image.open(im)
        # except IOError:
        #     continue
        new_surface = pygame.image.load(image_list[i]).convert()
        for i in range(0,int(LCD_WIDTH/10)):

            screen.blit(new_surface, (0,0,i*10+10, LCD_HEIGHT), (0,0,i*10+10,LCD_HEIGHT))
            pygame.display.update()
            pygame.time.wait(10)

#     for im in image_list:
#         try:
#             next_image = Image.open(im)
#         except IOError:
#             continue
