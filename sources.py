import copy
import json
import typing
import requests
cache = {}
cache["employees"] = {}

API_URL_ROOT = 'https://rfy56yfcwk.execute-api.us-west-1.amazonaws.com/bigcorp'

def employees(limit,offset):
    #TODO: get lists from cache as well
    if offset:
      offset_url_part = '&offset=' + offset
    else:
      offset_url_part = ''

    employees = requests.get(f'{API_URL_ROOT}/employees?limit={limit}{offset_url_part}').json()
    _cache_employees_from_api(employees)
    return employees

def employee(employee_id):
  return _get_employee_from_cache_or_api(employee_id)

def _cache_employees_from_api(employees):
  global cache
  for employee in employees:
    cache["employees"][employee["id"]] = employee

def _get_employee_from_cache_or_api(employee_id:int):
  global cache
  if employee_id not in cache["employees"]:
    cache["employees"][employee_id] = _get_employee_from_external_api(employee_id)
  return copy.deepcopy(cache["employees"][employee_id])

def _get_employee_from_external_api(employee_id):
  return requests.get(f'{API_URL_ROOT}/employees?id={employee_id}').json()[0]


def load_file_from_disk_or_cache(file: str,force_read:bool = False):
  global cache
  if file not in cache:
    with open(file,'r') as f:
      cache[file] = json.loads(f.read())

  # A deep copy provides side effect safety at the expense of duplicating the file in memory.
  return copy.deepcopy(cache[file])

def offices() -> typing.List[typing.Dict]:
  return load_file_from_disk_or_cache('offices.json')

def departments() -> typing.List[typing.Dict]:
  return load_file_from_disk_or_cache('departments.json')

def office(office_id):
  return offices()[office_id-1]

def department(department_id):
  return departments()[department_id-1]


