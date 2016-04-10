import ujson
import util.airpy_logger as logger


def load_config_file(file_name):
    with open(file_name, 'r') as f:
        config_file = ujson.loads(f.readall())
    return config_file


def save_config_file(config_file, config):
    try:
        with open(config_file, 'w') as f:
            config_json = ujson.dumps(config)
            f.write("%s" % config_json)
    except:
        logger.error("Failed to save config file:{}".format(config_file))
