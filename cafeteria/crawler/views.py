from .dormitory_apply import dormitory
from .serializers import DormitorySerializer
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from .Haksik import restaurant, dor_restaurant
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
        try:
            if serializer.is_valid():
                if '비밀번호 입력' in e:
                    return Response({
                        "message": e,
                    }, status=status.HTTP_200_OK)
                elif '비밀번호 5회' in e:
                    return Response({
                        "message": e,
                    }, status=status.HTTP_200_OK)
                elif '같은 기간에 신청한 내역이 존재합니다.' in e:
                    return Response({
                        "message": e,
                    }, status=status.HTTP_200_OK)
                elif '생활관생만 이용 가능합니다.' in e:
                    return Response({
                        "message": e,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "message": "ok",
                    }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": e}, status.HTTP_200_OK)


class RestaurantView(APIView):

    def get(self, request):

        ddoock, il, rice, yang, noodle, faculty_menu = restaurant()
        breakfast, dinner = dor_restaurant()
        return Response({
            "뚝배기": ddoock,
            "일품": il,
            "덮밥": rice,
            "양식": yang,
            "면류": noodle,
            "교직원식단": faculty_menu,
            "조식": breakfast,
            "석식": dinner,
        })
