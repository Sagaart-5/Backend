from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Art
from .serializers import ArtSerializer, SellArtSerializer, EvaluationSerializer
from users.models import CustomUser


class ArtViewSet(viewsets.ModelViewSet):
    """Класс для работы с моделью Art."""

    queryset = Art.objects.all()
    serializer_class = ArtSerializer


@api_view(["POST"])
def sell_art_object(request):
    """Выставление объекта искусства на продажу."""

    if request.method == "POST":
        serializer = SellArtSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            response_data = {
                "success": True,
                "message": "Art object listed for sale successfully"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "message": "Invalid input data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def evaluate_art_object(request):
    """Получение оценки стоимости объекта искусства."""

    if request.method == "POST":
        serializer = EvaluationSerializer(data=request.data)
        if serializer.is_valid():
            objectId = serializer.validated_data["objectId"]

            art_object = get_object_or_404(Art, id=objectId)

            # Логика оценки стоимости
            estimated_value = 1000000  # Пример
            currency = "USD"

            response_data = {
                "success": True,
                "estimatedValue": estimated_value,
                "currency": currency,
                "message": "Art object evaluated successfully"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "message": "Invalid input data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def purchase_art_object(request):
    """Покупка объекта искусства."""

    if request.method == "POST":
        objectId = request.data.get("objectId")
        buyerId = request.data.get("buyerId")

        # Проверка, существует ли объект искусства с заданным objectId
        art_object = get_object_or_404(Art, id=objectId)

        # Проверка, был ли объект уже продан
        if art_object.sold:
            return Response({
                "success": False,
                "message": "Object is already sold"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            buyer = CustomUser.objects.get(id=buyerId)
        except CustomUser.DoesNotExist:
            return Response({
                "success": False,
                "message": "Buyer not found"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Проверка, что покупатель не является автором объекта
        if buyer.email == art_object.author_name:
            return Response({
                "success": False,
                "message": "The author cannot purchase their own art object"
            }, status=status.HTTP_400_BAD_REQUEST)

        art_object.sold = True
        art_object.save()

        response_data = {
            "success": True,
            "message": "Object purchased successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)
