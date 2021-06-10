# pygenx
A thin python wrapper around GenX

# Installation

## Dependencies

`pygenx` requires:
- An installation of Julia 1.3.x (https://julialang.org/downloads/oldreleases/)
- A cloned repository of GenX (https://github.com/GenXProject/GenX)

## Installing pygenx
Install `pygenx` via `pip install .` or `pipenv install`.

## Configuring pygenx

To configure within python:
```python
import pygenx
pygenx.configure()
```

To configure from the command-line:
```shell
python path_to_pygenx_package/configure.py
```

The configuration process will prompt you for the location of the installed Julia 1.3 executable and the GenX repository.
The configuration of the Python/Julia communication may take several minutes.
At the end, you should see a message `configuration successful!`.

# Using pygenx to launch GenX models
Currently, `pygenx` is set up to launch existing `Run.jl` scripts within a GenX project folder,
or to produce a simple `Run.jl` script from a template, which assumes a certain file structure in that folder:
- A `Setting` subdirectory, containing a `genx_settings.yml` file and a file for the settings of the chosen solver.
- Input data files in the same directory at the `Run.jl` file.

To run within python:
```python
import pygenx
pygenx.run(genx_project_directory)
```

If a `Run.jl` file is not present in `genx_project_directory`, one will be created automatically, unless `make_runfile=Fasle`:
```python
import pygenx
pygenx.run(genx_project_directory, make_runfile=False)
```

If no `Run.jl` file is present, and `make_runfile=False`, an error will be raised.

To run from the command-line:
```shell
python path_to_pygenx_package/run.py path_to_genx_project
```
