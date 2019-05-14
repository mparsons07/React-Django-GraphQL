# We will create a query "hello" that returns string "world"

import graphene
import json

# Create graphen root query class with subclass graphene.
class Query(graphene.ObjectType):
	# First argument is hello of type string
	hello = graphene.String()

	# Is the new user admin?
	is_admin = graphene.Boolean()

	# How to obtain the string world? using resolvers, with snake_case notation
	def resolve_hello(self, info):
		return 'world'

	def resolve_is_admin(self, info):
		return True

# Create the schema based on the query type
schema = graphene.Schema(query = Query)
# Execute the query
result = schema.execute(
	# Pass the graphql object as parameter
	'''
	{
		hello
	}
	'''
)
# Print the results
print(result.data.items())
# odict_items([('hello', 'world')])
print(result.data['hello'])
# world -> returns just the ouput
# Print result in json format.
# First store a dictionary
dictResult = dict(result.data.items())
print(json.dumps(dictResult, indent = 2))
# indent = 2 makes more readable the output


# Query admin values
result = schema.execute(
	# Pass the graphql object as parameter
	# IMPORTANTE: executes must be passed in camelCase notation
	'''
	{
		isAdmin
	}
	'''
)
print(result.data.items())

# Disable camel case
schema = graphene.Schema(query = Query, auto_camelcase = False)
result = schema.execute(
	'''
	{
		is_admin
	}
	'''
)
print('Same as before: ', result.data.items())
