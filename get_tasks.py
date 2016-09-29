# coding: utf-8
import todoist as td
import pandas as pd
import os
import os.path as op
import shutil


def flush_cache(location=None):
    if location is None:
        location = op.join(op.expanduser('~'), ".todoist-sync")
    if op.exists(location) and op.isdir(location):
        shutil.rmtree(location)


def get_tasks_by_project(api, p_id):
    complete = api.items.get_completed(p_id)
    incomplete = api.projects.get_data(p_id)
    return complete + incomplete['items']

if __name__ == '__main__':
    flush_cache()
    api = td.TodoistAPI(os.environ['TODOIST_SECRET'])
    resp = api.sync()
    project_ids = [x['id'] for x in resp['projects']]
    tasks = []
    for p_id in project_ids:
        tasks.extend(get_tasks_by_project(api, p_id))
    df = pd.DataFrame.from_records(tasks)
    df.to_csv("tasks.tsv", index=False, sep='\t')
