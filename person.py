from flask import Flask
from flask_restful import Api, Resource, abort, reqparse


app = Flask(__name__)
api = Api(app)

#people = {1: {'name': 'John', 'age': '27', 'sex': 'Male'},
        #  2: {'name': 'Marie', 'age': '22', 'sex': 'Female'}}


people = {
    'person1': {'name': 'jenniffer',
    'cpf': '123.456.789-09', 
    'cellphone': '(21) 9 7454-6131', 
    'address': 'Rua Coronel Tamarindo, 8',
    },
    'person2': {
        'name': 'milena',
        'cpf': '123.456.789-09',
        'cellphone': '(21) 9 7454-6131',
        'address': 'Rua dos Lindos, 88',
    },
}

def abort_if_person_not_present(person_id):
    if person_id not in people:
        abort(404, message="Sorry, the person you're looking for doesn't exist!".format(person_id))

parser = reqparse.RequestParser()
parser.add_argument('person')

class Person(Resource):
    #get a specific person
    def get(self, person_id):
       abort_if_person_not_present(person_id)
       return people[person_id]

    #delete a specific person
    def delete(self, person_id):
        abort_if_person_not_present(person_id)
        del people[person_id]
        return '', 204

    #updates a specific person
    def put(self, person_id):
        args = parser.parse_args()
        person = {
        'name': args['name'],
        'cpf': args['cpf'],
        'cellphone': args['cellphone'],
        'address': args['address'],
        }
        people[person_id] = person
        return person, 201


#methods belonging to the list of people
class People(Resource):
    #gets the list of people
    def get(self):
        return people

    def post(self):
        args = parser.parse_args()
        person_id = int(max(people.keys()).lstrip('person')) + 1 #basically catches the maximum element in the list and adds 1 to it
        person_id = 'person%i' % person_id
        #TODOS[todo_id] = {'task': args['task']}
        people[person_id] = {'name': args['name'],'cpf': args['cpf'], 'cellphone': args['cellphone'], 'address': args['address']}
        return people[person_id], 201



#add the path to the routes
api.add_resource(People, '/people') #list of people
api.add_resource(Person, '/people/<person_id>') #an individual person 

if __name__ == '__main__':
    app.run(debug=True)
