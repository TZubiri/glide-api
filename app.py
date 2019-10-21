import flask
import requests
app = flask.Flask('glide')
API_URL_ROOT = 'https://rfy56yfcwk.execute-api.us-west-1.amazonaws.com/bigcorp'

@app.route("/employees")
def employees():
  #TODO: check status code
  #TODO: Choose best proxying mechanism, text might contain unicode magic.
  #TODO: Set header as text/json

  limit = flask.request.args.get('limit')
  #TODO: Return user error on non positive integer inputs.
  if limit == None :
    limit = 100
  elif int(limit) > 1000:
    limit = '1000'
  #TODO: What happens on negative inputs?

  if offset:= flask.request.args.get('offset'):
    offset_url_part = '&offset=' + offset
  else:
    offset_url_part = ''

  return requests.get(f'{API_URL_ROOT}/employees?limit={limit}{offset_url_part}').text,200,{'content-type':'application/json'}

@app.route('/employees/<int:employee_id>')
def employee(employee_id):
  return requests.get(f'{API_URL_ROOT}/employees?id={employee_id}').text,200,{'content-type':'application/json'}

#TODO: Serve app through apache or nginx
if __name__ == "__main__":
  app.run(host='0.0.0.0')