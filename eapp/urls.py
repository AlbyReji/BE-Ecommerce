from django.urls import path 
from .import views
from django.contrib.auth import views as auth
# from eapp.views import index




urlpatterns = [
    # path('',index.as_view(), name='index'),
    path('',views.index , name = 'index'),

    path('base/',views.base , name = 'base'),
    path('login/',views.login , name = 'login'),
    path('logout/',auth.LogoutView.as_view(template_name = 'eapp_temp/index.html'),name="logout"),
    path('register/',views.register , name = 'register'),
    path('adminhome/',views.adminhome , name = 'adminhome'),
    path('remove_cart/<str:cid>',views.remove_cart , name = 'remove_cart'),
    path('addcategory/',views.admin_add_category , name = 'admin_add_category'),
    path('addproduct/',views.admin_add_product , name = 'admin_add_product'),
    path('userhome/',views.userhome , name = 'userhome'),
    path('userhome/<str:name>',views.productview,name="userhome"),
    path('userhome/<str:cname>/<str:pname>',views.productdetails,name="productdetails"),
    path('addtocart/',views.add_to_cart , name = 'addtocart'),
    path('cart_page/',views.cart_page , name = 'cart_page'),
    path('userprofile/',views.userprofile , name = 'userprofile'),
    path('order_view/',views.order_view , name = 'order_view'),
    path('place_order/',views.place_order , name = 'place_order'),









]