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


def flush_cache(location=None):
    if location is None:
        location = op.join(op.expanduser('~'), ".todoist-sync")
    if op.exists(location) and op.isdir(location):
        shutil.rmtree(location)


def get_tasks_by_project(api, p_id):
    return api.projects.get_data(p_id)['items']

if __name__ == '__main__':
    flush_cache()
    api = td.TodoistAPI(os.environ['TODOIST_SECRET'])
    resp = api.sync()
    offset = 0
    batch_tasks = api.completed.get_all(limit=50, offset=offset)['items']
    task_accumulator = batch_tasks
    while len(batch_tasks) == 50:
        offset += 1
        batch_tasks = api.completed.get_all(limit=50,
                offset=(50 * offset))['items']
        task_accumulator.extend(batch_tasks)
    completed_df = pd.DataFrame.from_records(task_accumulator)
    completed_df.to_csv("completed.tsv", encoding="utf-8", index=False, sep='\t')

    # current stack
    project_ids = [x['id'] for x in resp['projects']]
    tasks = []
    for p_id in project_ids:
        tasks.extend(get_tasks_by_project(api, p_id))
    current_df = pd.DataFrame.from_records(tasks)
    current_df.to_csv("tasks.tsv", encoding="utf-8", index=False, sep='\t')
    embed()
