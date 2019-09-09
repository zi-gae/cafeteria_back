import os
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings


class ReactAppView(View):

    def get(self, request):
        try:
            with open(os.path.join("/Users/user/Documents/git_repo/cafeteria_front", "build", "index.html")) as file:
                return HttpResponse(file.read())
        except:
            return HttpResponse(
                """
                index.html not found!! build your react app
                """,
                status=501
            )
