from django.contrib import admin
from django.utils.html import format_html # html escape를 없애준다.
from .models import Order
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('fcuser', 'product', 'styled_status')
    list_filter = ('status',) # 필터 넣어주는 방법

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