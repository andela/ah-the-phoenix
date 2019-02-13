from rest_framework.decorators import renderer_classes, api_view
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
import coreapi
from rest_framework import response

# API definitions
@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    schema = coreapi.Document(
        title='Authors Haven API',
        url='localhost:8000',
        content={
            'users': {
                'create_user': coreapi.Link(
                    url='/api/v1/users/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='username',
                            required=True,
                            location='form',
                            description='Name of the user.'
                        ),
                        coreapi.Field(
                            name='email',
                            required=True,
                            location='form',
                            description='Email of the user.'
                        ),
                        coreapi.Field(
                            name='password',
                            required=True,
                            location='form',
                            description='Password of the user.'
                        )
                    ],
                    description='Create a User Account.'
                ),
                'login_user': coreapi.Link(
                    url='/api/v1/users/login/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='username',
                            required=True,
                            location='form',
                            description='Enter Name of the user.'
                        ),
                        coreapi.Field(
                            name='password',
                            required=True,
                            location='form',
                            description='Enter the password of User.'
                        )
                    ],
                    description='Login a User.'
                ),
                'get_user': coreapi.Link(
                    url='/api/v1/user/',
                    action='GET',
                    description='Show all of the users details.',
                ),
                'update_user': coreapi.Link(
                    url='/api/v1/user/',
                    action='PUT',
                    fields=[
                        coreapi.Field(
                            name='username',
                            required=True,
                            location='form',
                            description='New name to be updated'
                        ),
                        coreapi.Field(
                            name='bio',
                            required=True,
                            location='form',
                            description='Short Description about the User.'
                        ),
                        coreapi.Field(
                            name='image',
                            required=True,
                            location='form',
                            description='The Image url of the user.'
                        )
                    ],
                    description='Update a Users Details.',
                ),

            }
        }
    )
    return response.Response(schema)
