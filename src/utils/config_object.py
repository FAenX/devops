from .config import DevopsConfig

config = DevopsConfig()

def config_object():
    return config.read_config_file()