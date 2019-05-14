# We will create a query "hello" that returns string "world"

import graphene
import json
import uuid
from datetime import datetime

class User(graphene.ObjectType):
	# user data
	id = graphene.ID(default_value=str(uuid.uuid4()))
	username = graphene.String()
	created_at = graphene.DateTime(default_value=datetime.now())


# Create graphen root query class with subclass graphene.
class Query(graphene.ObjectType):
	# In order to create a query that lists all users
	# Introduce limit for paginate results
	users = graphene.List(User, limit=graphene.Int())

	# Is the new user admin?
	is_admin = graphene.Boolean()

	def resolve_is_admin(self, info):
		return True

	def resolve_users(self, info, limit=None):
		# Making limit=None we make the input value optional
		return [
			User(id="1", username="Fred", created_at=datetime.now()),
			User(id="2", username="Matias", created_at=datetime.now()),
			User(id="3", username="June", created_at=datetime.now())
		][:limit]

class CreateUser(graphene.Mutation):
	user = graphene.Field(User)
	# as we did with queries parameters passed to mutations are declared as follows
	class Arguments:
		username = graphene.String()

	# what do we do with this mutation subclass and username?
	# create the user! always called like this
	def mutate(self, info, username):
		# we dont need to define id or created_at as they have a default value
		user = User(username=username)
		return CreateUser(user=user)

# add new users
# Mutation root class
class Mutation(graphene.ObjectType):
	# class.Field() inside root mutation
	create_user = CreateUser.Field()

# add mutation to schema for creating a user
schema = graphene.Schema(query=Query, mutation=Mutation)
result = schema.execute(
	'''
	mutation ($username: String ) {
		createUser(username: $username) {
			user {
				id 
				username
				createdAt
			}
		}
	}
	''',
    variable_values={
        "username": "Jeff"
    }
)
dictResult = dict(result.data.items())
print(json.dumps(dictResult, indent = 2))


# Create the schema based on the query type
# schema = graphene.Schema(query = Query)
# Execute the query
result = schema.execute(
	# Pass the graphql object as parameter
	'''
	query getUsersQuery ($limit: Int) {
		users (limit: $limit) {
			id
			username
			createdAt
		}
	}
	''',
    variable_values={
        "limit": 1
    }
)

# First store a dictionary
dictResult = dict(result.data.items())
print(json.dumps(dictResult, indent = 2))
# indent = 2 makes more readable the output