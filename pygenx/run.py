import inspect
import os
import sys

from julia.api import LibJulia

import pygenx
from pygenx.configure import load_configuration


def run(folder_path=None, make_runfile=True):
    """Launch a Julia session, using the configured julia/python communication, and use
    this session to run the code present in 'Run.jl', or use a template 'Run.jl' file.

    :param str folder_path: path to GenX project files. If None, use current working
    directory.
    :param bool make_runfile: If a file named Run.jl is not present, whether it should
        be created.
    :raises ValueError: if a file named 'Run.jl' is not present in the GenX project
        folder and ``make_runfile`` is False.
    """
    # Python-side configuration
    folder_path = os.getcwd() if folder_path is None else folder_path
    config = load_configuration()
    runfile_location = os.path.join(folder_path, "Run.jl")
    if not os.path.isfile(runfile_location):
        if make_runfile:
            pygenx_root = os.path.dirname(inspect.getfile(pygenx))
            run_template_path = os.path.join(pygenx_root, "Run.jl")
            with open(run_template_path, "r") as f:
                run_template = f.read().splitlines()
            run_template = run_template.replace("$GENX_REPO_PATH", config["genx_path"])
            with open(runfile_location, "w") as f:
                f.write(run_template)
        else:
            raise ValueError("Run.jl does not exist, and make_runfile is False")
    # Launch the configured julia executable and GenX environment
    api = LibJulia.load(julia=config["julia_exec"])
    api.init_julia([f"--project={config['genx_path']}"])
    from julia import Pkg

    Pkg.activate(config["genx_path"])
    from julia import Main

    Main.runfile_path = runfile_location
    Main.eval("include(runfile_path)")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run(sys.argv[1])
    else:
        run()
