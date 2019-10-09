from .dormitory_apply import dormitory
from .serializers import DormitorySerializer
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from .Haksik import restaurant
from rest_framework.views import APIView


class OutApply(GenericAPIView):

    serializer_class = DormitorySerializer

    def post(self, request):
        serializer = DormitorySerializer(data=request.data)
        tu_id = request.data.get("tu_id")
        tu_password = request.data.get("tu_password")
        first_day = request.data.get("first_day")
        second_day = request.data.get("second_day")
        apply_text = request.data.get("apply_text")
        e = dormitory(tu_id, tu_password, first_day, second_day, apply_text)
        if serializer.is_valid():
            if '비밀번호 입력' in e:
                return Response({
                    "message": e,
                }, status=status.HTTP_401_UNAUTHORIZED)
            elif '비밀번호 5회' in e:
                return Response({
                    "message": e,
                }, status=status.HTTP_403_FORBIDDEN)
            elif '같은 기간에 신청한 내역이 존재합니다.' in e:
                return Response({
                    "message": e,
                }, status=status.HTTP_406_NOT_ACCEPTABLE)
            elif '생활관생만 이용 가능합니다.' in e:
                return Response({
                    "message": e,
                }, status=status.HTTP_402_PAYMENT_REQUIRED)
            else:
                return Response({
                    "message": e,
                }, status=status.HTTP_200_OK)


class RestaurantView(APIView):

    def get(self, request):
        if '식단' in restaurant():
            message = restaurant()
            return Response({
                'message': message,
            })
        else:
            ddoock, il, rice, yang, noodle, faculty_menu = restaurant()
            return Response({
                "뚝배기": ddoock,
                "일품": il,
                "덮밥": rice,
                "양식": yang,
                "면류": noodle,
                "교직원": faculty_menu,
            })
