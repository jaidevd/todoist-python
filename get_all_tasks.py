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
import pandas as pd
import shutil
from IPython import embed

RECURRING_PREFIXES = "every weekly yearly monthly".split()


def is_recurring(item):
    date_string = item['date_string']
    if date_string:
        for prefix in RECURRING_PREFIXES:
            if date_string.startswith(prefix):
                return True
    return False


def flush_cache(location=None):
    if location is None:
        location = op.join(op.expanduser('~'), ".todoist-sync")
    if op.exists(location) and op.isdir(location):
        shutil.rmtree(location)


def get_tasks_by_project(api, p_id):
    return api.projects.get_data(p_id)['items']


def get_history(api):
    offset = 0
    batch_tasks = api.completed.get_all(limit=50, offset=offset)['items']
    task_accumulator = batch_tasks
    while len(batch_tasks) == 50:
        offset += 1
        batch_tasks = api.completed.get_all(limit=50,
                offset=(50 * offset))['items']
        task_accumulator.extend(batch_tasks)
    return task_accumulator


if __name__ == '__main__':
    flush_cache()
    api = td.TodoistAPI(os.environ['TODOIST_SECRET'])
    resp = api.sync()
    completed_items = get_history(api)
    completed_df = pd.DataFrame.from_records(completed_items)
    completed_df.to_csv("completed.tsv", encoding="utf-8", index=False, sep='\t')

    # current stack
    project_ids = [x['id'] for x in resp['projects']]
    tasks = []
    for p_id in project_ids:
        tasks.extend(get_tasks_by_project(api, p_id))
    current_df = pd.DataFrame.from_records(tasks)
    current_df.to_csv("tasks.tsv", encoding="utf-8", index=False, sep='\t')
    embed()
