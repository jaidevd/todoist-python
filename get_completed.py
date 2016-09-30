#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Cube26 product code
#
# (C) Copyright 2015 Cube26 Software Pvt Ltd
# All right reserved.
#
# This file is confidential and NOT open source.  Do not distribute.
#

"""

"""

import todoist as td
import os
import os.path as op
import shutil


def flush_cache(location=None):
    if location is None:
        location = op.join(op.expanduser('~'), ".todoist-sync")
    if op.exists(location) and op.isdir(location):
        shutil.rmtree(location)

if __name__ == '__main__':
    flush_cache()
    api = td.TodoistAPI(os.environ['TODOIST_SECRET'])
    resp = api.sync()
    offset = 0
    batch_tasks = api.completed.get_all(limit=50, offset=offset)['items']
    task_accumulator = batch_tasks
    while len(batch_tasks) == 50:
        offset += 1
        print offset
        batch_tasks = api.completed.get_all(limit=50,
                offset=(50 * offset))['items']
        task_accumulator.extend(batch_tasks)
    print len(task_accumulator)
