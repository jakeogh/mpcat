#!/usr/bin/env python3
# -*- coding: utf8 -*-
# tab-width:4

from __future__ import annotations

import os
from collections.abc import Sequence
from math import inf
from pathlib import Path
from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal

import click
from asserttool import ic
from clicktool import click_add_options
from clicktool import click_global_options
from clicktool import tvicgvd
from globalverbose import gvd
from mptool import output
from unmp import unmp

signal(SIGPIPE, SIG_DFL)


def mpcat(
    path: Path,
    *,
    verbose: bool = False,
) -> Sequence:
    _path = Path(os.fsdecode(path))

    ic(_path)
    with open(_path, "rb") as fh:
        path_content_iterator = unmp(
            file_handle=fh,
            valid_types=[
                tuple,
                bytes,
                str,
                dict,
            ],
            verbose=gvd,
        )
        for thing in path_content_iterator:
            if gvd:
                ic(thing)
            yield thing


@click.command()
@click.argument(
    "paths",
    type=click.Path(
        exists=True,
        dir_okay=False,
        file_okay=False,
        allow_dash=False,
        path_type=Path,
    ),
    nargs=-1,
    required=True,
)
@click_add_options(click_global_options)
@click.pass_context
def cli(
    ctx,
    paths: tuple[Path, ...],
    verbose_inf: bool,
    dict_output: bool,
    verbose: bool = False,
) -> None:
    tty, verbose = tvicgvd(
        ctx=ctx,
        verbose=verbose,
        verbose_inf=verbose_inf,
        ic=ic,
        gvd=gvd,
    )

    if paths:
        iterator = paths
    else:
        iterator = unmp(
            valid_types=[
                bytes,
            ],
            verbose=bool(gvd),
        )
    del paths

    index = 0
    for index, path in enumerate(iterator):
        ic(index, path)
        for thing in mpcat(path):
            output(
                thing, reason=path, dict_output=dict_output, tty=tty, verbose=bool(gvd)
            )
