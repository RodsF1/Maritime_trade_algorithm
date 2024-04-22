# type: ignore
# FIXME: this file is incomplete


import sys

from invoke import task

if False:

    @task
    def activatevenv(c, bash=False):
        if sys.platform.startswith("win") or sys.platform.startswith("cygwin"):
            # rod case
            cmd = ".\.venv\Scripts\activate.bat"
        elif sys.platform.startswith("darwin") or sys.platform.startswith("linux"):
            # ben case
            cmd = "source .venv/bin/activate"
            if not bash:
                cmd += ".fish"
        else:
            raise RuntimeError("Unknown platform, cannot set up virtual environment")
