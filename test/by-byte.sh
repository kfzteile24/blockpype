#!/bin/sh

test/setup.sh

. .venv/bin/activate ; cat test/40lines.txt | python blockpype/cli.py -b 10 python test/pid_prepend.py