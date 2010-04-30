#!/usr/bin/env python
# -*- coding: Latin-1 -*-

LABELMATCH = r".*\label{(.*)}.*"
MESSAGE = "Label '%s' -- (%d, %s), already defined in -- (%d, %s)"

import re
import fileinput

from glob import glob

texfiles = glob('*.tex')
file_reader = fileinput.input(texfiles)

labels = dict()

for line in file_reader:
    match = re.match(LABELMATCH, line)
    if match != None:
        label = match.groups()[0]
        current_file = file_reader.filename()
        current_line = file_reader.filelineno()
        if label in labels:
            old_line, old_file = labels[label]
            print MESSAGE % (label, current_line, current_file, old_line,
                    old_file)
        else:
            labels[label] = (current_line, current_file)
