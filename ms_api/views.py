from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.db.models import Q
from .models import *
import requests


def default(request):

    context = {
        'info': ['/post/?id={postID} - to get Post by its ID',
                 '/post/?userId={userID} - to get all Posts by the User']
    }
    return render(request, 'ms_api/home.html', context)


@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def posts(request):

    if request.GET.__contains__('id'):                          # GET with post ID
        post_id_raw = request.GET.get('id')
        context_400 = {
            "error": [{"message": "400 BAD REQUEST"}]
        }
                                                                # check if the parameter is numerical
                                                                # or greater than 0 or lesser than 101
        if not post_id_raw.isnumeric() or int(post_id_raw) <= 0:
            return Response(context_400, status=status.HTTP_400_BAD_REQUEST, template_name='ms_api/index.html')
        else:
            post_id = int(post_id_raw)                          # get post with id or original_post_id matching post_id
            post = Post.objects.filter(Q(id=post_id) | Q(original_post_id=post_id))

            if len(post) != 0:                                  # if the post exists
                context = {
                    "data": post
                }
                return Response(context, status=status.HTTP_200_OK, template_name='ms_api/index.html')
            else:
                                                                # chceck if post_id isn't greater that 100
                if post_id > 100:                               # because the External API posts IDs go only up to 100
                    return Response(context_400, status=status.HTTP_400_BAD_REQUEST, template_name='ms_api/index.html')
                else:
                    post = f'https://jsonplaceholder.typicode.com/posts/{post_id}'
                    res = requests.get(post)
                    api_post = res.json()

                    new_post = Post(user_id=int(api_post['userId']), title=str(api_post['title']),
                                    body=str(api_post['body']), original_post_id=int(api_post['id']))
                    new_post.save()
                    context = {
                        "data": {new_post}
                    }
                    return Response(context, status=status.HTTP_201_CREATED, template_name='ms_api/index.html')

    elif request.GET.__contains__('userId'):                    # GET with user ID
        user_id_raw = request.GET.get('userId')

        if not user_id_raw.isnumeric():                         # check if the parameter is numerical
            context = {
                "error": [{"message": "400 BAD REQUEST - userId not integer"}]
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST, template_name='ms_api/index.html')
        else:
            user_id = int(user_id_raw)
            post = Post.objects.filter(user_id=user_id)         # get all post from the user

            if post.count() == 0:
                context = {
                    "error": [{"message": "400 BAD REQUEST - user made no posts"}]
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST, template_name='ms_api/index.html')
            else:
                context = {
                    "data": post
                }
                return Response(context, status=status.HTTP_200_OK, template_name='ms_api/index.html')
    else:
        context_404 = {
            "error": [{"message": "404 NOT FOUND"}]
        }
        return Response(context_404, status=status.HTTP_404_NOT_FOUND, template_name='ms_api/index.html')


@api_view(['POST'])
def add_post(request):

    try:
        if "user_id" not in request.data or "title" not in request.data or "body" not in request.data:
            return Response({"message": "parameters missing in request body"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user_id = request.data['user_id']
            if not isinstance(user_id, int):
                return Response({"message": "user_id is not integer"}, status=status.HTTP_400_BAD_REQUEST)

            user = f'https://jsonplaceholder.typicode.com/users/{user_id}'
            res = requests.get(user)
            api_user = res.json()

            if len(api_user) == 0:                              # checking if user_id is in external API
                return Response({"user_id": user_id, "message": "non valid user_id"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                new_post = Post(user_id=user_id, title=str(request.data['title']), body=str(request.data['body']),
                                original_post_id=None)
                new_post.save()
                return Response({"id": new_post.id, "message": "new post created"}, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_post(request, post_id):

    try:
        post = Post.objects.get(id=post_id)
        post.delete()
        return Response({"id": post_id, "message": "post deleted successfully"}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({"id": post_id, "message": "post not found"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def put_post(request):

    if "id" not in request.data or "body" not in request.data or "title" not in request.data:
        return Response({"message": "parameters missing in request body"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        post_id = request.data['id']
        post = Post.objects.filter(id=post_id)
        if post.count() == 0:
            return Response({"id": post_id, "message": "post not found"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            post.update(body=str(request.data['body']), title=str(request.data['title']))
            return Response({"message": "post updated successfully"}, status=status.HTTP_200_OK)
