from urllib import response
from flask import Flask, request
from flask_cors import CORS
from deploy_react_app import deploy_react_app
from utils.config import DevopsConfig
from database.database_queries import Database

# for now, we will use a global variable to store the data
config = DevopsConfig()
config = config()
print(config)


app = Flask(__name__)

CORS(app)

@app.route("/")
def hello():
    return "Hello World!"

# post /deploy/react
@app.route("/deploy/", methods=["POST"])
def deploy():
    print(request.get_json())
    data = request.get_json()
    app = data['app']
    if app == 'react':
        project_name = data['projectName'].lower().replace(' ', '-').lower()
        results = deploy_react_app(project_name)
        return results

    return 'Not implemented'

@app.route("/projects", methods=["GET"])
def get_projects():
    database = Database(connector='sqlserver')
    results = database.execute_query('select top 5 * from projects order by 1 desc')
    return results



if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0')