import yaml


class Config(object):
    """
    Class to handle the configuration given with `--config` option.
    """

    def __init__(self):
        """
        generate an empty config when no input config file provided.
        """

        self.config = ""

    def config_from_file(self, config_file):
        """
        stores the configuration from file to a config object.
        """

        with open(config_file) as config_file:
            self.config = yaml.safe_load(config_file)

    def write_config(self):
        """
        writes the config object to a file in block format.
        """

        with open('config.yml', 'w') as outfile:
            outfile.write(yaml.dump(self.config, default_flow_style=False))

    def print_config(self):
        """
        returns the config object as a string.
        """

        return yaml.dump(self.config)
