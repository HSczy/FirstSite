from django.shortcuts import render
from django.db.models import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import LikeRecord, LikeCount


# Create your views here

def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


def SUCCESSResponse(like_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['like_num'] = like_num
    return JsonResponse(data)


def like_change(request):
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400, '喜欢这个内容？赶快登录点赞吧！')

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))

    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_object = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401, '点赞对象不存在')
    # 数据处理

    if request.GET.get('is_liked') == 'true':
        # 要点赞
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id,
                                                                user=user)
        if created:
            # 未点赞，进行点赞
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.like_num += 1
            like_count.save()
            return SUCCESSResponse(like_count.like_num)
        else:
            # 已点赞，不能重复点赞
            return ErrorResponse(402, '您的喜欢我们已经记录，多谢')
    else:
        # 取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            # 已点赞 取消点赞
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()

            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if created:
                # 无点赞数据，数据错误
                return ErrorResponse(404, '数据错误')
            else:
                # 点赞数减一
                like_count.like_num -= 1
                like_count.save()
                return SUCCESSResponse(like_count.like_num)

        else:
            # 未点赞，不能取消点赞
            return ErrorResponse(403, '未点赞，不能取消点赞')
