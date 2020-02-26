from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify

# initialize list to hold students records as dictionary in format {"id": 101 , "name": "Jaspreet" } 
students_list = [{"id": 1, "name": "Bob Smith"}, {"id": 2, "name": "John Doe"}]

# initialize classes list to hold records as dictionary 
# in format {"id": 201 , "name": "CMPE273" , students : [{"id": 101 , "name": "Jaspreet" }] } 
classes_list = [{"id": 1, "name": "CMPE202", "students": []}, {"id": 2, "name": "CMPE272", "students": []}]

# starting student id from 100 and class id from 200
sid = 100
cid = 200

app = Flask(__name__)

type_defs = load_schema_from_path('schema.graphql')

#Setting the QueryType()
query = ObjectType("Query")
students = ObjectType('Student')
classes = ObjectType('Classes')
mutation = ObjectType("Mutation")

#Setting the Query fields
@query.field("students")	
# GET method for displaying the student record at given student id
def resolve_students(_,info,id):	
	students_result = [index for index in students_list if index["id"]== int(id)]
	return students_result

@query.field("classes")
# GET method for displaying the class record at given class id
def resolve_classes(_,info,id):	
	class_result = [index for index in classes_list if index["id"]==int(id)]
	return class_result

@query.field("studentsList")
#shows list of all students
def resolve_studentsList(_,info):
	return students_list

@query.field("classesList")
#shows list of all classes
def resolve_classesList(_,info):
	return classes_list


#Setting the Mutation fields
@mutation.field("newStudent")
def resolve_newStudent(_,info,name):
	global sid
	new_student = { "id" : sid , "name" : name }
	students_list.append(new_student)
	sid = sid + 1
	return new_student

@mutation.field("newClass")
# POST method for adding new class record and storing it in the classes_list , with class id auto incremented by 1 
def resolve_newClass(_,info,name):
	global cid
	new_class = { "id" : cid , "name" : name , "students" : [] }
	classes_list.append(new_class)
	cid = cid + 1 
	return new_class 

@mutation.field("updateClass")
def resolve_updateClass(_,info,class_id,student_id):
# Method to update the record and add the students with student_id in the class at a given class_id 
	for index in classes_list:
		if (index["id"]==class_id):
			for ind in students_list:
				if ind["id"] == student_id :
					index["students"].append(ind)
	
	updateResult=[index for index in classes_list if index["id"]==class_id]
	return updateResult

schema = make_executable_schema(type_defs, [query, students, classes, mutation])

@app.route('/graphql', methods=['GET'])
def playground():
    return PLAYGROUND_HTML, 200
    
@app.route('/graphql', methods=['POST'])
def run_server():
    inputs = request.get_json()
    success, result = graphql_sync(
    schema,
    inputs,
    context_value=request,
    debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code
