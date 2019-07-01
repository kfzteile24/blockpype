#!/usr/bin/env bash

if [ ! -d .venv ] ; then
    python -m virtualenv -p python3 .venv
fi
