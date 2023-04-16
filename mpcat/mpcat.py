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
from clicktool import tv
from mptool import output
from unmp import unmp

signal(SIGPIPE, SIG_DFL)


def mpcat(
    path,
    *,
    verbose: bool | int | float = False,
) -> Sequence:
    _path = Path(os.fsdecode(path))

    if verbose:
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
            verbose=verbose,
        )
        for thing in path_content_iterator:
            if verbose == inf:
                ic(thing)
            yield thing


@click.command()
@click.argument("paths", type=str, nargs=-1)
@click_add_options(click_global_options)
@click.pass_context
def cli(
    ctx,
    paths: tuple[str, ...],
    verbose_inf: bool,
    dict_output: bool,
    verbose: bool | int | float = False,
) -> None:
    tty, verbose = tv(
        ctx=ctx,
        verbose=verbose,
        verbose_inf=verbose_inf,
    )

    if paths:
        iterator = paths
    else:
        iterator = unmp(
            valid_types=[
                bytes,
            ],
            verbose=verbose,
        )
    del paths

    index = 0
    for index, path in enumerate(iterator):
        if verbose:
            ic(index, path)
        for thing in mpcat(path, verbose=verbose):
            output(
                thing, reason=path, dict_output=dict_output, tty=tty, verbose=verbose
            )
