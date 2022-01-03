from django.contrib import admin
from .models import Order, OrderLineItem


# OrderLineItemAdminInline inherits from admin.TabularInline
# allows us to add and edit line items in the admin
# right from inside the order model.
class OrderLineItemAdminInline(admin.TabularInline):
    """ Lineitem total """
    model = OrderLineItem
    # lineitem_total is read only
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    """ Setup fields """
    inlines = (OrderLineItemAdminInline,)

    # These fields are all things that will be calculated by our model methods.
    # Including order number, date, delivery cost, order total, and
    # grand_total. So we don't want anyone to have the ability to edit them
    readonly_fields = ('order_number', 'date',
                       'discount_amount', 'order_total',
                       'grand_total', 'original_bag',
                       'stripe_pid')

    # allows us to specify the order of fields - as per the model
    fields = ('order_number', 'user_profile', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'discount_amount',
              'order_total', 'grand_total', 'original_bag',
              'stripe_pid')

    # restrict columns that are visible in the order list
    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'discount_amount',
                    'grand_total',)

    # most recent orders at the top
    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
