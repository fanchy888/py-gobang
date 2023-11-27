import yaml
import os


def load():
    path = os.path.dirname(os.path.abspath(__file__))
    with open(path + '/config.yaml') as f:
        cfg_data = f.read()
    return yaml.load(cfg_data, Loader=yaml.FullLoader)


class Config:
    def __init__(self):
        self.cfg = load()['olo']

    @property
    def host(self):
        return self.cfg['host']


config = Config()
