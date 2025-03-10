{ pkgs }: {
  deps = [
    pkgs.unixODBC
    pkgs.freetype
    pkgs.glibcLocales
    pkgs.python3Packages.flask
    pkgs.python3Packages.pandas
    pkgs.python3Packages.reportlab
  ];
}

modules = ["python-3.12", "web"]
run = "gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app"

[nix]
channel = "stable-24_05"

[deployment]
run = ["sh", "-c", "gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app"]

[[ports]]
localPort = 5000
externalPort = 5000
exposeLocalhost = true

[[package]]
name = "flask"
version = "3.1.0"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "blinker" },
    { name = "click" },
    { name = "itsdangerous" },
    { name = "jinja2" },
    { name = "werkzeug" },
]

[project]
name = "repl-nix-workspace"
version = "0.1.0"
description = "Add your description here"
requires-python = ">=3.12"
dependencies = [
    "flask>=3.1.0",
    "pandas>=2.2.3",
    "reportlab>=4.3.1",
]
