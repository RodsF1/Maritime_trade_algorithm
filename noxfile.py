# NOTE: this was copied straight from the nox docs
#  https://nox.thea.codes/en/stable/cookbook.html#recipes

import os
import pathlib
import sys

import nox  # type: ignore

# It's a good idea to keep your dev session out of the default list
# so it's not run twice accidentally
# nox.options.sessions = [...]  # Sessions other than 'dev'

# this VENV_DIR constant specifies the name of the dir that the `dev`
# session will create, containing the virtualenv;
# the `resolve()` makes it portable
VENV_DIR = os.path.join(os.getcwd(), ".venv")


@nox.session
def dev(session: nox.Session) -> None:
    """
    Sets up a python development environment for the project.

    This session will:
    - Create a python virtualenv for the session
    - Install the `virtualenv` cli tool into this environment
    - Use `virtualenv` to create a global project virtual environment
    - Invoke the python interpreter from the global project environment to install
      the project and all it's development dependencies.
    """
    if (
        sys.platform.startswith("aix")
        or sys.platform.startswith("wasi")
        or sys.platform.startswith("emscri")
    ):  # third one is emscripten (idk why the fuck we would be running that here but just in case??)
        raise RuntimeError("ERROR: unsupported platform")

    session.install("virtualenv")  # this guy was actually not the problem
    session.run(
        "virtualenv", os.fsdecode(VENV_DIR), silent=False
    )  # both this line and the one above should work

    # set defaults to ben's version
    (exe_dir, python_exe_ext) = (
        ("Scripts", ".exe")
        if (sys.platform.startswith("win") or sys.platform.startswith("cygwin"))
        else ("bin", "")
    )
    python = os.path.join(VENV_DIR, exe_dir, f"python{python_exe_ext}")

    assert os.path.isfile(python), "ERROR: paths still not working"  # this should do it

    # Use the venv's interpreter to install the project along with
    # all it's dev dependencies, this ensures it's installed in the right way
    session.run(
        python,
        "-m",
        "pip",
        "install",
        "pip-chill",
        "pip-tools",
        "pipdeptree",
        "pipreqs",
        "setuptools",  # just in case
        external=True,
    )

    _path_pipchill = os.path.join(VENV_DIR, exe_dir, f"pip-chill{python_exe_ext}")
    _path_pipcompile = os.path.join(VENV_DIR, exe_dir, f"pip-compile{python_exe_ext}")
    _path_pipsync = os.path.join(VENV_DIR, exe_dir, f"pip-sync{python_exe_ext}")

    # session.run(_path_pipchill, ">", "_tmp.txt")  # NOTE: only uncomment this this line if you had any changes made to the reqs list
    session.run(
        _path_pipcompile,
        "-vv",
        "--emit-options",
        "--emit-index-url",
        "--annotate",
        "--header",
        "--emit-trusted-host",
        "-o" "requirements.lock.txt",
        "requirements.txt",
    )  # this guy will resolve any dependency issues and create the .lock file

    session.run(_path_pipsync, "requirements.lock.txt")
    # now you should have a fully ready to go dev environment

    print(
        "all set!  now activate the venv -> for windows: .\\.venv\\Scripts\\activate.bat"
    )
