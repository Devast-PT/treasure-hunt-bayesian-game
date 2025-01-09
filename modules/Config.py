import yaml
import os

class Config:
    def __init__(self):
        with open(r'modules/config.yaml', 'r') as file:

            config = yaml.safe_load(file)
            self.width = config['App']['size']['width']
            self.height = config['App']['size']['height']
            self.title = config['App']['title']
            self.font_overall = (
                config['App']['overall']['font'],
                config['App']['overall']['font_size']
            )


    @staticmethod
    def static_gamedata():
        with open(r'modules/config.yaml', 'r') as file:
            config = yaml.safe_load(file)
            data = {'rows': config['App']['gamedata']['rows'], 'columns': config['App']['gamedata']['columns']}
            return data
