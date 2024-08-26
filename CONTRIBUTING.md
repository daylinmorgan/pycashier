# Contributing

Thanks you for your interest in contributing to the development of `pycashier`!

See below for getting started editing the `pycashier` source or documentation.
Please submit an issue with a detailed bug report or feature request prior to opening any pull requests.

## Setup Environment

> [!NOTE]
> Most important development tasks are covered by recipes within the [`Makefile`](./Makefile).
> See `make help` for more info.

The development for `pycashier` is managed by [`pixi`](https://github.com/prefix-dev/pixi).
You can use the included `Makefile` to setup `pixi` envs and `pre-commit`.

```sh
make env
pixi shell -e dev
```

Or directly calling the commands invoked my `make env`:

```sh
pixi install -e dev
pixi run -e dev pre-commit install
pixi shell -e dev
```

> [!NOTE]
> There is a hidden `pycashier` command to check for runtime dependencies: `pycashier checks`.

## Editing Source

### Running Tests

The current test suite focuses on integration tests of the main CLI
using known inputs/output files.

After making any changes to the source you can run tests
with `pytest` or using the below command:

Any additional functionality or feature should be covered by an integration test using known inputs/outputs.

```sh
make test
```

## Documentation

The documentation is written in `markdown` and built using `sphinx`.
If you setup your environment as described above then you can
live preview changes by running the following:

```sh
make docs-serve
```
