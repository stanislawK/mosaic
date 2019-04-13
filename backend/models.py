from random import shuffle


class MosaicModel:

    def __init__(self, randomly=0, resolution=(2048, 2048)):
        self.randomly = randomly
        self.resolution = resolution
        self.images = []

    def add_images(self, images_str):
        self.images = images_str.split(',')
        if self.randomly == 1:
            shuffle(self.images)

    def add_resolution(self, resolution_str):
        self.resolution = tuple([int(x) for x in resolution_str.split('x')])
