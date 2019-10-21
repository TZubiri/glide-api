import flask

app = flask.Flask('glide')
API_URL_ROOT = 'https://rfy56yfcwk.execute-api.us-west-1.amazonaws.com/bigcorp'

@app.route("/")
def hello():
  a = 2+2
  return "Hello World!"

if __name__ == "__main__":
  app.run(host='0.0.0.0')