from django.urls import reverse
from django.contrib.contenttypes.fields import ContentType
from django.http import JsonResponse
from .forms import CommentForm
from .models import Comment


# Create your views here.

def comment_update(request):
    data = {}
    comment_form = CommentForm(request.POST, comment_user=request.user)

    if comment_form.is_valid():
        comment = Comment()
        content_type = comment_form.cleaned_data['content_type']
        content_type = ContentType.objects.get(model=content_type)
        object_id = comment_form.cleaned_data['object_id']
        comment.content_object = comment_form.cleaned_data['content_object']
        comment.comment_user = comment_form.cleaned_data['comment_user']
        comment.text = comment_form.cleaned_data['comment']
        parent = comment_form.cleaned_data['parent']
        if parent is not None:
            comment.root = parent.root if parent.root is not None else parent
            comment.parent = parent
            comment.reply_to = parent.comment_user
        comment.save()
        # return redirect(referer)
        data['status'] = 'SUCCESS'
        data['comment_user'] = comment.comment_user.get_nickname()
        data['created_time'] = comment.created_time.strftime('%Y-%m-%d %H:%M:%S')
        data['text'] = comment.get_md_text()
        if parent is not None:
            data['reply_to'] = comment.reply_to.get_nickname()
            if comment.reply_to.is_superuser:
                data['extend_reply_to'] = '[博主]'
            else:
                data['extend_reply_to'] = ''
        else:
            data['reply_to'] = ''
            data['extend_reply_to'] = ''

        if comment.comment_user.is_superuser:
            data['extend_user'] = '[博主]'
        else:
            data['extend_user'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if comment.root is not None else ''
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        data['img_url'] = comment.comment_user.get_avatar()
        data['comment_count'] = Comment.objects.filter(content_type=content_type, object_id=object_id).count()

    else:
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)
