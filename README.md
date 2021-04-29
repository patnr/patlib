# patlib

Purposes:

- Share tools across my projects, such as DAPPER.
- Define optional dependencies to setup my dev. environments by
  "inheriting" from here. The aim is that I only need to keep
  pylib up to date (e.g. pinning buggy Jedi or pdbpp),
  rather than the `pyproject.toml` of each and every project.

  ```toml
  [tool.poetry.dev-dependencies]
  # Either:
  patlib = {version = "==0.2.8", extras = ["mydev", "misc"]}
  # Or:
  patlib = {path = "../../py/patlib", extras = ["mydev", "misc"], develop=true}
  ```

  NB: Maybe this is a bad idea; maybe I will forget to include e.g.
  numpy when publishing the other project.

- Provide pylab replacement: from patlib.all import *
