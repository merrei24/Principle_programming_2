from configparser import ConfigParser

def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    if not parser.has_section(section):
        raise Exception("Section not found in database.ini")

    config = {}
    for param in parser.items(section):
        config[param[0]] = param[1]

    return config