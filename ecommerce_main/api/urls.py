from django.urls import path
from . import views

urlpatterns = [
    path("filter_products/<str:field>/<str:query>/",views.filter_products,name="filter_products"),
    path("products/<int:id>",views.get_product,name="get_product"),
    path("add_to_cart/<int:user_id>/<int:product_id>",views.add_product_to_cart,name="add_product_to_cart"),
    path("remove_from_cart/<int:user_id>/<int:product_id>",views.remove_product_from_cart,name="remove_product_from_cart"),
    path("my_cart/<int:user_id>/",view=views.get_my_cart,name="get_my_cart"),
    path("place_order/<int:buyer_id>/<int:product_id>",views.place_order,name="place_order"),
    path("cancel_order/<int:order_id>/",view=views.cancel_order,name="cancel_order"),
    path("my_orders/<int:user_id>/",views.get_my_orders,name="get_my_orders"),
    path("get_profile/<int:user_id>",views.get_my_profile,name="get_my_profile"),
    path("delete_user/<int:user_id>",views.delete_user,name="delete_user"),
    path("check-username-existence",views.check_username_existence,name="check_username_existence"), 
    path("check-email-existence",views.check_email_existence,name="check_email_existence"),
    path("register",views.register,name="register"),
    path("login",views.login_user,name="login"),
    path("check-password",views.check_password,name="check_password"),
    path('logout',views.logout_user,name="logout"),
    path('set-password',views.set_password,name="set_password"),
    path("change-address",views.change_address,name="change_address"),
]