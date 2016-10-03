# coding: utf-8
import get_all_tasks as gat
import os
from todoist import TodoistAPI

gat.flush_cache()
api = TodoistAPI(os.environ['TODOIST_SECRET'])
resp = api.sync()
items = resp['items']
item = items[-1]
manager = api.items
x = manager.get_completed(item['project_id'])

kaggle_completed = api.items.get_completed(item['project_id'])
ieeg_completed = []

for completed in kaggle_completed:
    if item['content'] == completed['content']:
        ieeg_completed.append(completed)

for completed in kaggle_completed:
    print completed.get('content')

for item in items:
    if "iEEG" in item.get('content'):
        print item
        break

ieeg_id = 58071361
gotten_content = manager.get(ieeg_id)

for k, v in item.iteritems():
    if v != gotten_content['item'].get(k):
        print k, v
        print k, gotten_content['item'].get(k)

history = gat.get_history(api)
for h in history:
    if h['id'] == ieeg_id:
        print h['completed_date']

for task in items:
    if gat.is_recurring(task):
        print task['content']

for task in history:
    if "pysemantic mysql" in task['content']:
        print task
        break
history_payload = []

for task in history:
    payload = api.items.get(task['id'])
    if payload is None:
        print task['content']
    else:
        history_payload.append(payload)
