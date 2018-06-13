from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html
from .models import Order, OrderItem
import csv
import datetime


def order_pdf(obj):
    return format_html('<a href="{}">PDF</a>'.format(
        reverse('orders:admin_order_pdf', args=[obj.id])
    ))

order_pdf.short_description = 'В PDF'


def order_detail(obj):
    return format_html('<a href="{}">Посмотреть</a>'.format(
        reverse('orders:admin_order_detail', args=[obj.id])
    ))


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv', charset='utf-8')
    response['Content-Disposition'] = 'attachment; \
        filename=Orders-{}.csv'.format(datetime.datetime.now().strftime("%d/%m/%Y"))
    writer = csv.writer(response, delimiter='|', dialect='excel')

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export CSV'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_field = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address',
                    'postal_code', 'city', 'paid', 'created', 'updated',
                    order_detail, order_pdf]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]


admin.site.register(Order, OrderAdmin)
