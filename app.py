import flask
import requests
import json
import typing
import copy


app = flask.Flask('glide')
API_URL_ROOT = 'https://rfy56yfcwk.execute-api.us-west-1.amazonaws.com/bigcorp'
cache = {}
cache["employees"] = {}

@app.route("/employees")
def employees():
  #TODO: check status code
  #TODO: Choose best proxying mechanism, text might contain unicode magic.
  #TODO: Set header as text/json

  limit = flask.request.args.get('limit',default = '100')
  #TODO: Return user error on non positive integer inputs.
  if int(limit) > 1000:
    limit = '1000'
  #TODO: What happens on negative inputs?

  if offset := flask.request.args.get('offset'):
    offset_url_part = '&offset=' + offset
  else:
    offset_url_part = ''

  employees = requests.get(f'{API_URL_ROOT}/employees?limit={limit}{offset_url_part}').json()
  _cache_employees_from_api(employees)
  expanded_employees = expand(employees,flask.request.args.getlist('expand'))
  return json.dumps(expanded_employees) ,\
          200,{'content-type':'application/json'}


@app.route('/employees/<int:employee_id>')
def parse_employee(employee_id):
  return expand([employee(employee_id)],flask.request.args.getlist('expand'))[0],\
         200, {'content-type': 'application/json'}

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


@app.route('/departments')
def departments():
  limit,offset = parse_args(flask.request.args)
  selected_departments = departments_json()[offset:offset+limit]
  expanded_selected_departments = expand(selected_departments,flask.request.args.getlist('expand'))
  return json.dumps(expanded_selected_departments),\
         200, {'content-type': 'application/json'}

@app.route('/departments/<int:department_id>')
def parse_department(department_id):
  return expand([department(department_id)],flask.request.args.getlist('expand'))[0],\
         200, {'content-type': 'application/json'}

def department(department_id):
  return departments_json()[department_id-1]


@app.route('/offices')
def offices():
  limit,offset = parse_args(flask.request.args)
  selected_offices = offices_json()[offset:offset+limit]
  expanded_selected_offices = expand(selected_offices,flask.request.args.getlist('expand'))
  return json.dumps(expanded_selected_offices),\
         200, {'content-type': 'application/json'}

@app.route('/offices/<int:office_id>')
def parse_office(office_id):
  return expand([office(office_id)],flask.request.args.getlist('expand'))[0],\
         200, {'content-type': 'application/json'}

def office(office_id):
  return offices_json()[office_id-1]

def parse_args(args):
  limit = args.get('limit',default='100')
  offset = args.get('offset',default='0')
  limit = int(limit)
  offset = int(offset)
  limit = min(1000,limit)

  return limit,offset

def load_file_from_disk_or_cache(file: str,force_read:bool = False):
  global cache
  if file not in cache:
    with open(file,'r') as f:
      cache[file] = json.loads(f.read())

  # A deep copy provides side effect safety at the expense of duplicating the file in memory.
  return copy.deepcopy(cache[file])

def offices_json():
  return load_file_from_disk_or_cache('offices.json')
def departments_json() -> typing.List[typing.Dict]:
  return load_file_from_disk_or_cache('departments.json')

@app.route('/reload_data/4jz06v155')
def read_json_files():
  load_file_from_disk_or_cache('offices.json',force_read=True)
  load_file_from_disk_or_cache('departments.json',force_read =True)

def get_object_by_key_and_id(key,id):
  key_to_func = {}
  key_to_func["manager"] = employee;
  key_to_func["office"] = office;
  key_to_func["department"] = department;
  key_to_func["superdepartment"] = department;

  return key_to_func[key](id)

def expand(objects_to_expand: typing.List,list_of_list_of_keys_to_expand):

  objects_to_expand = copy.deepcopy(objects_to_expand)
  for list_of_keys_to_expand in list_of_list_of_keys_to_expand:
    for object_to_expand in objects_to_expand:
      for key_to_expand in list_of_keys_to_expand.split('.'):

      #TODO: Check if field exists.
      #TODO: Check if field is an id.
        if key_to_expand in object_to_expand:
          id_to_expand = object_to_expand[key_to_expand]
          if id_to_expand is None:
            break
          #skip expansion if value is already expanded.
          elif type(id_to_expand) is int:
            object_to_expand[key_to_expand] = get_object_by_key_and_id(key_to_expand,id_to_expand)

          object_to_expand = object_to_expand[key_to_expand]

  return objects_to_expand


#TODO: Serve app through apache or nginx
if __name__ == "__main__":
  read_json_files()
  app.run(host='0.0.0.0')
