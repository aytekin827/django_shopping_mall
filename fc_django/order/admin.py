import datetime
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.db.models import F, Q
from django.contrib import admin
from django.utils.html import format_html # html escape를 없애준다.
from django.db import transaction
from django.template.response import TemplateResponse
from django.urls import path
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
    list_display = ('fcuser', 'product', 'styled_status','action')
    list_filter = ('status',) # 필터 넣어주는 방법
    change_list_template = 'admin/order_change_list.html'
    change_form_template = 'admin/order_change_form.html'

    actions = [
        refund
    ]

    def action(self,obj):
        if obj.status != '환불':
            return format_html(f'<input type="button" value="환불" onclick="order_refund_submit({obj.id})" class="btn btn-primary btn-sm">')

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

        if request.method == 'POST':
            # print(request.POST)
            obj_id = request.POST.get('obj_id')
            if obj_id:
                qs = Order.objects.filter(pk=obj_id)
                ct = ContentType.objects.get_for_model(qs.model)
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

        return super().changelist_view(request, extra_context)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        order = Order.objects.get(pk=object_id)
        extra_context = { 'title' : f"'{order.fcuser.email}'의 '{order.product.name}' 수정하기"}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super().changeform_view(request, object_id, form_url, extra_context)

    def get_urls(self):
        urls = super().get_urls()
        date_urls = [
            path('date_view/', self.date_view),
        ]
        return date_urls + urls

    def date_view(self, request):
        week_date = datetime.datetime.now() - datetime.timedelta(days=7)
        week_data = Order.objects.filter(register_date__gte=week_date) # __gte : '크거나 같음'
        data = Order.objects.filter(register_date__lt = week_date) # __lt : '작음'
        context = dict(
            self.admin_site.each_context(request),
            week_data = week_data,
            data = data
        )
        return TemplateResponse(request, 'admin/order_date_view.html', context)
admin.site.register(Order, OrderAdmin)