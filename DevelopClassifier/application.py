from controller.development_system import DevelopmentSystem
from dotenv import load_dotenv

#app = Flask(__name__)
#api = Api(app)
load_dotenv()
"""
class HelloWorld(Resource):
    def get(self):
        return Response()
    def post(self):
        some_json = request.get_json()
        return {'you sent ': some_json}, 201

class Multi(Resource):
    def get(self, num):
        return {'result ': num * 10}



# The file in "file_path" will be sent due to a GET request on the endpoint "/get_file"
@app.route("/get_file", methods=['GET'])
def test():
    file_path = 'data/preprocessedDataset.csv'
    return send_file(file_path, as_attachment=True)


api.add_resource(HelloWorld, '/')
api.add_resource(Multi, '/multi/<int:num>')
"""
if __name__ == '__main__':
    print("CIAO SONO NEL MAIL")
    DevelopmentSystem().run()
    print("run done")
    #app.run(host="0.0.0.0" ,port=6000, debug=True)
