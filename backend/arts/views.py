from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Art
from .serializers import ArtSerializer, SellArtSerializer


class ArtViewSet(viewsets.ModelViewSet):
    """Класс для работы с моделью Art."""

    queryset = Art.objects.all()
    serializer_class = ArtSerializer


@api_view(["POST"])
def sell_art_object(request):
    if request.method == "POST":
        serializer = SellArtSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            response_data = {
                "success": True,
                "message": "Арт-объект успешно выставлен на продажу"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "message": "Неверные данные",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
