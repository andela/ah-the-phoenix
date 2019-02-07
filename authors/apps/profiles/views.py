from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfilesSerializer



class ProfileUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfilesSerializer

    def get(self, request, username, *args, **kwargs):
        try:
            profile = Profile.objects.select_related('user').get(
                user__username=username
            )
        except Exception:
            raise NotFound("The requested profile was not found")

        serializer = self.serializer_class(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def patch(self, request, username):
        if request.user.username != username:
            response = {
                    "message": "You don't have permission to edit this profile"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        serializer = self.serializer_class(instance=request.user.profile,
                                        data=data, partial=True)
        if serializer.is_valid():
            self.check_object_permissions(request, data)
            serializer.save()
            return Response(serializer.data)
        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileGetAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ProfilesSerializer
    queryset = Profile.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ProfilesSerializer(queryset, many=True)
        return Response({"Profiles":serializer.data})
