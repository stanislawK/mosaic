from random import shuffle


class MosaicModel:

    def __init__(self, randomly=0, resolution=(2048, 2048)):
        self.randomly = randomly
        self.resolution = resolution
        self.images = []

    def add_images(self, images_str):
        self.images = images_str.split(',')
        if self.randomly == '1':
            shuffle(self.images)

    def add_resolution(self, res_str):
        try:
            self.resolution = tuple([int(x) for x in res_str.split('x')])
        except ValueError:
            self.resolution = (2048, 2048)
