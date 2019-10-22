import flask
import requests
import json
app = flask.Flask('glide')
API_URL_ROOT = 'https://rfy56yfcwk.execute-api.us-west-1.amazonaws.com/bigcorp'
cache = {}


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

  if offset:= flask.request.args.get('offset'):
    offset_url_part = '&offset=' + offset
  else:
    offset_url_part = ''

  return requests.get(f'{API_URL_ROOT}/employees?limit={limit}{offset_url_part}').text,\
          200,{'content-type':'application/json'}


@app.route('/employees/<int:employee_id>')
def employee(employee_id):
  return requests.get(f'{API_URL_ROOT}/employees?id={employee_id}').text,\
         200, {'content-type':'application/json'}


@app.route('/departments')
def departments():
  limit,offset = parse_args(flask.request.args)
  return json.dumps(departments_json()[offset:offset+limit]),\
         200, {'content-type': 'application/json'}

@app.route('/offices')
def offices():
  limit,offset = parse_args(flask.request.args)
  return json.dumps(offices_json()[offset:offset+limit]),\
         200, {'content-type': 'application/json'}

def parse_args(args):
  limit = args.get('limit',default='100')
  offset = args.get('offset',default='0')
  limit = int(limit)
  offset = int(offset)
  limit = min(1000,limit)

  return limit,offset
def load_file_from_memory_or_cache(file: str,force_read:bool = False):
  global cache
  if file not in cache:
    with open(file,'r') as f:
      cache[file] = json.loads(f.read())
  return cache[file]

def offices_json():
  return load_file_from_memory_or_cache('offices.json')
def departments_json():
  return load_file_from_memory_or_cache('departments.json')

@app.route('/reload_data/4jz06v155')
def read_json_files():
  load_file_from_memory_or_cache('offices.json',force_read=True)
  load_file_from_memory_or_cache('departments.json',force_read =True)


#TODO: Serve app through apache or nginx
if __name__ == "__main__":
  app.run(host='0.0.0.0')
  read_json_files()
