#!/usr/bin/env python
# Prepends current pid to the output block

import os, select, sys

print('')
print(f"PID: {os.getpid()}")
print(sys.argv)
sys.stderr.write("Sample stderr output\n")
print('')

if select.select([sys.stdin,],[],[],0.0)[0]:
    for line in sys.stdin.buffer:
        sys.stdout.buffer.write(line)
