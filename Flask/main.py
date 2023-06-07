from flask import Flask, render_template, url_for, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


@app.route('/')
# def index():
#   return render_template('index.html')
@app.route('/SendAPI', methods=['POST'])
def SendAPI():
    API_data = request.get_json()
    print(API_data) 
    results = {'status': API_data}
    return jsonify(results)

if __name__ == "__main__":
  app.run(debug=True)