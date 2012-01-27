class PHPObject(object):
    def __init__(self, name, **kwargs):
        self.param = kwargs
        self.name = name