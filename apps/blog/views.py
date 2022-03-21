from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from .serializers import PostSerializer
from .models import Post


class PostsAPIView(GenericAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get(self, request):
        posts = self.get_queryset()
        data = self.get_serializer(posts, many=True).data

        return Response(data={'posts': data},
                        status=status.HTTP_200_OK)


class PostAPIView(GenericAPIView):
    serializer_class = PostSerializer

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        data = self.get_serializer(post).data

        return Response(data={'post': data},
                        status=status.HTTP_200_OK)

