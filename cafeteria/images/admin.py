from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):

    # 어드민 패널 시작할때 보일 리스트 설정 하는 펑션
    list_display = (
        'id',
        'file',
        'title',
        'content',
        'creator',
        'kinds',
        'created_at',
        'updated_at',
    )

    # 눌렀을때 해당 링크로 가지 않고 수정창으로 감
    list_display_links = (
        'title',
        'content',
        'creator',
    )

    # 검색 창
    search_fields = (
        'content',
    )


@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'creator',
        'image',
        'created_at',
        'updated_at',
    )


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'message',
        'creator',
        'image',
        'created_at',
        'updated_at',
    )
    list_display_links = (
        'message',
    )
