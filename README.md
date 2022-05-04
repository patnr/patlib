# patlib

Should not be used in production code. Purposes:

- Expanded snippet (or "tips and tricks") library.
- Share tools across my projects, such as DAPPER.
- Provide common, version-controlled (and versioned) source
  of dependency specifications for various projects.

  Example:
  ```toml
  [tool.poetry.dev-dependencies]
  # Either:
  patlib = {version = "==0.2.8", extras = ["mydev", "misc"]}
  # Or:
  patlib = {path = "../../py/patlib", extras = ["mydev", "misc"], develop=true}
  ```

  NB: Not sure if good idea.
  Maybe you forget numpy when publishing a "dependant" project.
