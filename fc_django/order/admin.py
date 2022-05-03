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
    print(styled_status.__dict__)
    print(dir(styled_status))

    styled_status.short_description = '상태'

admin.site.register(Order, OrderAdmin)