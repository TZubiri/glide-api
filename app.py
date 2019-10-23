import flask
import json
import typing
import copy
import sources
from sources import load_file_from_disk_or_cache

app = flask.Flask('glide')

RESPONSE_HEADERS = {'content-type':'application/json'}


@app.route("/employees")
def parse_employees():
  #TODO: check status code
  #TODO: Choose best proxying mechanism, text might contain unicode magic.
  #TODO: Return user error on non positive integer inputs.
  #TODO: What happens on negative inputs?

  limit, offset = parse_args(flask.request.args)
  employees = sources.employees(limit,offset)
  expanded_employees = expand(employees,flask.request.args.getlist('expand'))
  return json.dumps(expanded_employees) ,\
          200, RESPONSE_HEADERS


@app.route('/employees/<int:employee_id>')
def parse_employee(employee_id):
  return expand([sources.employee(employee_id)],flask.request.args.getlist('expand'))[0],\
         200, RESPONSE_HEADERS


@app.route('/departments')
def parse_departments():
  limit,offset = parse_args(flask.request.args)
  selected_departments = sources.departments()[offset:offset+limit]
  expanded_selected_departments = expand(selected_departments,flask.request.args.getlist('expand'))
  return json.dumps(expanded_selected_departments), \
         200, RESPONSE_HEADERS

@app.route('/departments/<int:department_id>')
def parse_department(department_id):
  return expand([sources.department(department_id)],flask.request.args.getlist('expand'))[0],\
         200, RESPONSE_HEADERS

@app.route('/offices')
def parse_offices():
  limit,offset = parse_args(flask.request.args)
  selected_offices = sources.offices()[offset:offset+limit]
  expanded_selected_offices = expand(selected_offices,flask.request.args.getlist('expand'))
  return json.dumps(expanded_selected_offices), \
         200, RESPONSE_HEADERS


@app.route('/offices/<int:office_id>')
def parse_office(office_id):
  return expand([sources.office(office_id)],flask.request.args.getlist('expand'))[0],\
         200, RESPONSE_HEADERS

def parse_args(args):
  limit = args.get('limit',default='100')
  offset = args.get('offset',default='0')
  limit = int(limit)
  offset = int(offset)
  limit = min(1000,limit)

  return limit,offset



@app.route('/reload_data/4jz06v155')
def read_json_files():
  sources.load_file_from_disk_or_cache('offices.json', force_read=True)
  sources.load_file_from_disk_or_cache('departments.json', force_read =True)

def get_object_by_key_and_id(key,id):
  key_to_func = {}
  key_to_func["manager"] = sources.employee;
  key_to_func["office"] = sources.office;
  key_to_func["department"] = sources.department;
  key_to_func["superdepartment"] = sources.department;

  return key_to_func[key](id)

def expand(objects_to_expand: typing.List,list_of_list_of_keys_to_expand):

  #TODO: Bundle individual requests and send a bulk request to limit external api hits.

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


if __name__ == "__main__":
  read_json_files()
  app.run(host='0.0.0.0')
