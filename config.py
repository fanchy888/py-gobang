import yaml
import os


def load():
    path = os.path.dirname(os.path.abspath(__file__))
    with open(path + '/config.yaml') as f:
        cfg_data = f.read()
    return yaml.load(cfg_data, Loader=yaml.FullLoader)


class Config:
    def __init__(self):
        try:
            self.cfg = load()['olo']
        except Exception as e:
            self.cfg = {'host': 'ws://localhost:5555'}

    @property
    def host(self):
        return self.cfg['host']

    @property
    def rule(self):
        return self.cfg.get('rule', 19)


config = Config()
