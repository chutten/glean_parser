# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Console script for glean_parser."""

import io
from pathlib import Path
import sys

import click

from . import translate as mod_translate
from . import validate_ping


@click.command()
@click.argument(
    'input',
    type=click.Path(
        exists=True,
        dir_okay=False,
        file_okay=True,
        readable=True,
    ),
    nargs=-1
)
@click.option(
    '--output',
    '-o',
    type=click.Path(
        dir_okay=True,
        file_okay=False,
        writable=True,
    ),
    nargs=1,
    required=True,
)
@click.option(
    '--format',
    '-f',
    type=click.Choice(mod_translate.OUTPUTTERS.keys()),
    required=True,
)
def translate(input, format, output):
    """
    Translate metrics.yaml files to other formats.
    """
    sys.exit(
        mod_translate.translate(
            [Path(x) for x in input],
            format,
            Path(output)
        )
    )


@click.command()
@click.option(
    '--schema',
    '-s',
    type=str,
    default=validate_ping.PING_SCHEMA_DEFAULT_URL,
    nargs=1,
    required=False,
    help=(
        "HTTP url or file path to glean ping schema. "
        "If remote, will cache to disk."
    )
)
def check(schema):
    """
    Validate the contents of a glean ping.

    The ping contents are read from stdin, and the validation errors are
    written to stdout.
    """
    sys.exit(
        validate_ping.validate_ping(
            io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8'),
            io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8'),
            schema_url=schema
        )
    )


@click.group()
def main(args=None):
    """Command line utility for glean_parser."""
    pass


main.add_command(translate)
main.add_command(check)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
