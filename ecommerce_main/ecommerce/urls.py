from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('profile',views.profile_screen,name="profile_screen"),
    path("my-cart",views.my_cart_screen,name="my_cart_screen"),
    path("view-product/<int:product_id>",views.view_product_screen,name="view_product_screen"),
    path("search/<str:query>",views.search_result_screen,name="search_result_screen"),
    path("login",views.login_screen,name="login_screen"),
    path("register",views.register_screen_1,name="register_screen_1"),
    path("register/<str:username>/<str:email>",views.register_screen_2,name="register_screen_2"),
    path("previous-orders",views.previous_orders_screen,name="previous_orders_screen"),
    path("place-order/<int:product_id>",views.place_order_screen,name="place_order_screen"),
    path("place-order/<int:product_id>/delivery_address",views.place_order_screen_address,name="place_order_screen_address"),
    path("order-placed-success/<int:order_id>",views.order_placed_success,name="order_placed_success"),
    path("category/<int:category_id>",views.category_products,name="category_products"),
    path('change-password',views.password_reset,name="change-password"),
    path('change-password/password_reset_confirm/<str:uidb64>/<str:token>',views.set_password,name='password_reset_confirm'),

]