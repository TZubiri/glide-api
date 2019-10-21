import flask
import requests
app = flask.Flask('glide')
API_URL_ROOT = 'https://rfy56yfcwk.execute-api.us-west-1.amazonaws.com/bigcorp'

@app.route("/employees")
def employees():
  #TODO: check status code
  #TODO: Choose best proxying mechanism .text might contain unicode magic.
  #TODO: Set header as text/json
  return requests.get(API_URL_ROOT + '/employees').text

@app.route('/employees/<int:employee_id>')
def employee(employee_id):
  return requests.get(API_URL_ROOT + '/employees?id=' + str(employee_id)).text

if __name__ == "__main__":
  app.run(host='0.0.0.0')