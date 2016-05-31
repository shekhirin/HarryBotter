import yaml


class Config:
    def __init__(self, config_file='config.yml'):
        self.config_file = config_file
        self.config = yaml.load(open(config_file))

    def __getitem__(self, item):
        return self.config[item]

    def keys(self):
        return self.config.keys()

    def items(self):
        return self.config.items()
