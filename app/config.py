import yaml


path = './settings.yaml'

with open(path, 'r') as fd:
    settings = yaml.safe_load(fd)
