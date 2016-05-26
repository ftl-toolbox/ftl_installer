import os
import yaml

# used for opening config file.
USER_HOME = os.environ.get("HOME")


class Config(object):
    """
    Class to handle the configuration given with `--config` option.
    """

    def __init__(self, is_config_file=False):
        """
        generate an empty config when no input config file provided.
        """

        self.config = ""
        self.config_file = USER_HOME + "/.config/ftl_installer/ftl_installer.yml"

        if is_config_file:
            self.config_from_file()

    def __str__(self):
        """
        returns the config object as a string.
        """

        return yaml.dump(self.config, default_flow_style=False)

    def config_from_file(self):
        """
        stores the configuration from file to a config object.
        """

        try:
            with open(self.config_file) as config_file:
                self.config = yaml.safe_load(config_file)
        except IOError:
            with open(self.config_file, 'w') as config_file:
                config_file.write(yaml.dump(self.config, default_flow_style=False))

    def write_config(self):
        """
        writes the config object to a file in block format.
        """

        with open(self.config_file, 'w') as outfile:
            outfile.write(yaml.dump(self.config, default_flow_style=False))
