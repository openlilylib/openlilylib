# OpenLilyLib

Infrastructure for LilyPond add-ons

`OpenLilyLib` is a set of repositories providing extensions to
(LilyPond)[https://lilypond.org/]. This repository includes some of these as
submodules for ease of installation and updating.

## Installation

It is recommended that (git)[https://git-scm.com/] is used for installation.

First, choose a filesystem location for the code. You may already have a
directory for storing snippets of `LilyPond` code.

```sh
mkdir -p "$HOME/.local/share/lilypond"
```

Then change to that directory and clone this repository with `git`.

```sh
cd "$HOME/.local/share/lilypond"
git clone --recurse-submodules https://github.com/openlilylib/openlilylib
```

`LilyPond` can be instructed to include this directory in it's search path using
the `--include` or `-I` command line option. To save repeatedly typing this
path, you may wish to add the following to your shell initialization file, e.g.
`~/.bashrc`:

```sh
export OLLPATH="$HOME/.local/share/lilypond/openlilylib"
alias ollilypond='lilypond --include="$OLLPATH"'
```

Front-ends such as
(Frescobaldi)[https://www.frescobaldi.org/uguide#help_preferences_lilypond] may
have preference options to add this path when `LilyPond` is run.

## Usage

`OpenLilyLib` code is divided into packages and modules which can be loaded for
use by `LilyPond`. A typical file might look like this:

```lilypond
\version "2.23.81"

% oll core functions
\include "oll-core/package.ily"

% oll packages, e.g.:
\loadPackage edition-engraver

% oll modules, e.g.:
\loadModule oll-misc.pitch.auto-transpose

% your music
{ c' }
```

See the documentation in each git submodule for more details.

## Contributing

TODO add documentation.
