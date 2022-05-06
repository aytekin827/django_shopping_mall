from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.db.models import F, Q
from django.contrib import admin
from django.utils.html import format_html # html escape를 없애준다.
from django.db import transaction
from .models import Order
# Register your models here.

def refund(moodeladmin, request, queryset):
    # queryset의 변수에 어드민페이지에서 선택한 모델들이 들어온다.
    with transaction.atomic():
        qs = queryset.filter(~Q(status='환불'))
        ct = ContentType.objects.get_for_model(queryset.model)
        for obj in qs:
            obj.product.stock += obj.quantity
            obj.product.save()

            LogEntry.objects.log_action(
                user_id = request.user.id,
                content_type_id = ct.pk,
                object_id = obj.pk,
                object_repr = '주문 환불',
                action_flag = CHANGE,
                change_message='주문 환불'
            )
        qs.update(status='환불')

refund.short_description = '환불1'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('fcuser', 'product', 'styled_status')
    list_filter = ('status',) # 필터 넣어주는 방법

    actions = [
        refund
    ]

    def styled_status(self, obj):
        if obj.status == '환불':
            return format_html(f'<span style="color:red"><strong>{obj.status}</strong></span>')
        elif obj.status == '결제완료':
            return format_html(f'<span style="color:green"><strong>{obj.status}</strong></span>')
        else:
            return obj.status

    styled_status.short_description = '상태'

    def changelist_view(self, request, extra_context=None):
        extra_context = { 'title' : '주문 목록'}
        print(request)
        return super().changelist_view(request, extra_context)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        order = Order.objects.get(pk=object_id)
        extra_context = { 'title' : f"'{order.fcuser.email}'의 '{order.product.name}' 수정하기"}
        return super().changeform_view(request, object_id, form_url, extra_context)

admin.site.register(Order, OrderAdmin)