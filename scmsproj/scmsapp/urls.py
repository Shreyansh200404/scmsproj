from django.urls import path
from . import views
from django.urls import include



# from django.contrib.auth.views import (
#     LogoutView, 
#     PasswordResetView, 
#     PasswordResetDoneView, 
#     PasswordResetConfirmView,
#     PasswordResetCompleteView
# )


from django.urls import path
from . import views



from django.urls import path


from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)


urlpatterns = [
    path('', views.home, name='home'),
    path('register/',views.register, name='register'),
    
    path('login/', views.user_login, name='login'),
    path('captcha_image/', views.captcha_image, name='captcha_image'),

    path('dashboard/', views.dashboard, name='dashboard'),

    #path('customer/edit/<int:id>/', views.edit_customer, name='edit_customer'),

    #path('customer_delete/<int:customer_id>/', views.customer_delete, name='customer_delete'),
    #path('customer_delete/<int:customer_id>/', views.customer_delete, name='customer_delete'),

    path('customer_confirm_delete/<int:customer_id>/', views.customer_confirm_delete, name='customer_confirm_delete'),
    #path('logout/', views.user_logout, name='logout'),

    path('logout/',views.logout_view, name='logout'),



    #path('report/<int:year>/<int:month>/', views.monthly_report, name='monthly_report'),

    

    # path('password_reset/', PasswordResetView.as_view(template_name='password_reset.html'),name='password-reset'),
    # path('password_reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    # path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    # path('password_reset_complete/',PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
    # path('password-reset/', PasswordResetView.as_view(template_name='password_reset.html'),name='password-reset'),
    # path('password-reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    # path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    # path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),


    path('customer_create/', views.customer_create, name='customer_create'),
    path('customer_list/', views.customer_list, name='customer_list'),
    path('customer_detail/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('customer_update/<int:customer_id>/', views.customer_update, name='customer_update'),
    path('customer_delete/<int:customer_id>/', views.customer_confirm_delete, name='customer_delete'),
    
    path('supplier_create/', views.supplier_create, name='supplier_create'),
    path('supplier_list/', views.supplier_list, name='supplier_list'),
    path('supplier_detail/<int:supplier_id>/', views.supplier_detail, name='supplier_detail'),
    path('supplier_update/<int:supplier_id>/', views.supplier_update, name='supplier_update'),
    path('supplier_confirm_delete/<int:supplier_id>/', views.supplier_confirm_delete, name='supplier_confirm_delete'),


    path('material_create/', views.material_create, name='material_create'),
    path('material_list/', views.material_list, name='material_list'),
    path('material_detail/<int:material_id>/', views.material_detail, name='material_detail'),
    path('material_update/<int:material_id>/', views.material_update, name='material_update'),
    path('material_confirm_delete/<int:material_id>/', views.material_confirm_delete, name='material_confirm_delete'),

    path('stock_create/', views.stock_create, name='stock_create'),
    path('stock_list/', views.stock_list, name='stock_list'),
    path('stock_detail/<int:stock_id>/', views.stock_detail, name='stock_detail'),
    path('stock_update/<int:stock_id>/', views.stock_update, name='stock_update'),
    path('stock_confirm_delete/<int:stock_id>/', views.stock_confirm_delete, name='stock_confirm_delete'),  


    path('sales_create/', views.sales_create, name='sales_create'),
    path('sales_list/', views.sales_list, name='sales_list'),
    path('sales_detail/<int:sales_id>/', views.invoice_detail, name='sales_detail'),
    path('sales_update/<int:sales_id>/', views.sales_update, name='sales_update'),
    path('sales_confirm_delete/<int:sales_id>/', views.sales_confirm_delete, name='sales_confirm_delete'), 

    #path('invoice/',views.invoice_detail,name='invoice_details'),

    #path('invoice/<int:invoice_id>/',views.invoice_detail,name='invoice_detail'),

    path('purchase_create/', views.purchase_create, name='purchase_create'),
    path('purchase_list/', views.purchase_list, name='purchase_list'),
    path('purchase_detail/<int:purchase_id>/', views.purchase_detail, name='purchase_detail'),
    path('purchase_update/<int:purchase_id>/', views.purchase_update, name='purchase_update'),
    path('purchase_confirm_delete/<int:purchase_id>/', views.purchase_confirm_delete, name='purchase_confirm_delete'),


    path('expense_create/', views.expense_create, name='expense_create'),
    path('expense_list/', views.expense_list, name='expense_list'),
    path('expense_detail/<int:expense_id>/', views.expense_detail, name='expense_detail'),
    path('expense_update/<int:expense_id>/', views.expense_update, name='expense_update'),
    path('expense_confirm_delete/<int:expense_id>/', views.expense_confirm_delete, name='expense_confirm_delete'),


    # path('invoice_create/', views.invoice_create, name='invoice_create'),
    # path('invoice_list/', views.invoice_list, name='invoice_list'),
    # path('invoice_detail/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    # path('invoice_update/<int:invoice_id>/', views.invoice_update, name='invoice_update'),
    # path('invoice_confirm_delete/<int:invoice_id>/', views.invoice_confirm_delete, name='invoice_confirm_delete'),

    # path('invoiceitem_create/', views.invoice_item_create, name='invoiceitem_create'),
    # path('invoiceitem_list/', views.invoice_item_list, name='invoiceitem_list'),
    # path('invoiceitem_detail/<int:invoiceitem_id>/', views.invoice_item_detail, name='invoiceitem_detail'),
    # path('invoiceitem_update/<int:invoiceitem_id>/', views.invoice_item_update, name='invoiceitem_update'),
    # path('invoiceitem_confirm_delete/<int:invoiceitem_id>/', views.invoice_item_confirm_delete, name='invoiceitem_confirm_delete'),


    

    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('reset-password/', views.reset_password_view, name='reset_password'),



    path('overall_report/', views.overall_report, name='overall_report'),

]
