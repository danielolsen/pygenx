import os
import sys

from julia.api import LibJulia

from pygenx.configure import load_configuration


def run(folder_path=None):
    # Launch the configured julia executable and GenX environment
    config = load_configuration()
    api = LibJulia.load(julia=config["julia_exec"])
    api.init_julia([f"--project={config['genx_path']}"])
    from julia import Pkg

    Pkg.activate(config["genx_path"])
    from julia import Main

    folder_path = os.getcwd() if folder_path is None else folder_path
    Main.runfile_path = os.path.join(folder_path, "Run.jl")
    Main.eval("include(runfile_path)")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run(sys.argv[1])
    else:
        run()
