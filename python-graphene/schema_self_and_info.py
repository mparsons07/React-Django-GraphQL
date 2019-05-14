# We will create a query "hello" that returns string "world"

import graphene
import json
import uuid
from datetime import datetime

# Let users create posts
class Post(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()

class User(graphene.ObjectType):
    # user data
    id = graphene.ID(default_value=str(uuid.uuid4()))
    username = graphene.String()
    created_at = graphene.DateTime(default_value=datetime.now())
    # create new avatar parameter that is a combination of id and username,
    # as an example of self
    avatar_url = graphene.String()

    def resolve_avatar_url(self, info):
        return 'https://cloudinary.com/{}/{}'.format(self.username, self.id)


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

class CreatePost(graphene.Mutation):
    post = graphene.Field(Post)

    class Arguments:
        title = graphene.String()
        content = graphene.String()
    
    def mutate(self, info, title, content):
        # create post if user is anonymous. Example of info usage
        if info.context.get('is_anonymous'):
            raise Exception('Not authenticated!')
        post = Post(title=title, content=content)
        return CreatePost(post=post)

# add new users
# Mutation root class
class Mutation(graphene.ObjectType):
    # class.Field() inside root mutation
    create_user = CreateUser.Field()
    create_post = CreatePost.Field()

# add mutation to schema for creating a user
schema = graphene.Schema(query=Query, mutation=Mutation)
result = schema.execute(
	'''
	mutation {
        createPost(title:"Hello", content:"world") {
            post {
                title
                content
            }
        }
    }
	''',
    context = {
        # We want to prevent anonymous users to create posts
        "is_anonymous": True
    }
    # variable_values={
    #     "username": "Jeff"
    # }
)
dictResult = dict(result.data.items())
print(json.dumps(dictResult, indent = 2))


# get avatars
result = schema.execute(
	'''
	{
        users {
            id 
            username
            createdAt
            avatarUrl
        }
    }
	'''
)
dictResult = dict(result.data.items())
print(json.dumps(dictResult, indent = 2))

