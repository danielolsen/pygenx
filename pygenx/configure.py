import inspect
import os

import julia
import yaml
from julia.api import LibJulia

import pygenx


def get_julia_exec():
    """Prompt the user for a path to the julia executable.

    :return: (*str*) -- user-provided path.
    """
    while True:
        use_default_julia = input("Use default julia executable from path? (y/n) ")
        if use_default_julia.lower()[0] in {"y", "n"}:
            use_default_julia = use_default_julia == "y"
            break
        print("Invalid entry detected.")
    if use_default_julia:
        return "julia"
    else:
        while True:
            julia_path = input("Enter path to julia executable: ")
            if os.path.isfile(julia_path):
                break
            print("Invalid entry detected.")
        return julia_path


def get_genx_path():
    """Prompt the user for a path to the cloned GenX repository.

    :return: (*str*) -- user-provided path.
    """
    while True:
        genx_path = input("Enter path to GenX repository: ")
        if os.path.isdir(genx_path):
            break
        print("Invalid entry detected.")
    return genx_path


def load_configuration(config_filepath=None):
    """Load the configuration from the YAML file.

    :param str config_filepath: path to configuration file. If None, load from the
        pygenx repo.
    :return: (*dict*) -- user-provided path.
    """
    if config_filepath is None:
        # Load from default location
        pygenx_package_path = os.path.dirname(inspect.getfile(pygenx))
        config_filepath = os.path.join(pygenx_package_path, "config.yml")

    # Read configuration file
    with open(config_filepath, "r") as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
    if not {"julia_exec", "genx_path"} == set(config.keys()):
        print(set(config.keys()))
        raise ValueError(
            "Malformed config.yml file, keys must be 'julia_exec' and 'genx_path'"
        )

    return config


def write_configuration(config):
    """Write the configuration to a file in the pygenx repo for future uses.

    :param dict config: configuration options, keys are 'julia_exec' and 'genx_path'.
    """
    # Static paths
    pygenx_package_path = os.path.dirname(inspect.getfile(pygenx))
    config_filepath = os.path.join(pygenx_package_path, "config.yml")

    with open(config_filepath, "w") as f:
        yaml.dump(config, f)


def configure(config_filepath=None):
    """Load the configuration from the YAML file, prompt the user for missing entries,
    set up python/Julia communication, and save the resulting config file if necessary.

    :param str config_filepath: path to configuration file. If None, load from the
        pygenx repo. This is the location to which configurations are saved, if changes
        have been made.
    """
    # Load existing configuration
    config = load_configuration(config_filepath)

    write_config = False
    # Reconfigure the julia executable if necessary/desired
    if config["julia_exec"] is None:
        config["julia_exec"] = get_julia_exec()
        write_config = True
    else:
        print(f"configured julia executable: {config['julia_exec']}")
        while True:
            to_replace = input("Replace this executable with another? (y/n) ")
            if to_replace.lower()[0] in {"y", "n"}:
                to_replace = to_replace == "y"
                break
            print("Invalid entry detected.")
        if to_replace:
            config["julia_exec"] = get_julia_exec()
            write_config = True
    # Reconfigure the GenX path if necessary/desired
    if config["genx_path"] is None:
        config["genx_path"] = get_genx_path()
        write_config = True
    else:
        print(f"configured GenX repo path: {config['genx_path']}")
        while True:
            to_replace = input("Replace this path with another? (y/n) ")
            if to_replace.lower()[0] in {"y", "n"}:
                to_replace = to_replace == "y"
                break
            print("Invalid entry detected.")
        if to_replace:
            config["genx_path"] = get_genx_path()
            write_config = True

    # Ensure that python can talk to the desired Julia executable
    api = LibJulia.load(julia=config["julia_exec"])
    api.init_julia([f"--project={config['genx_path']}"])
    julia.install(julia=config["julia_exec"])
    from julia import Pkg

    Pkg.activate(config["genx_path"])
    Pkg.instantiate()

    # Re-write the configuration file if necessary
    if write_config:
        write_configuration(config)
    print("configuration successful!")


if __name__ == "__main__":
    configure()
