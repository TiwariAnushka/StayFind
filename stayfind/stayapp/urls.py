from django.urls import path
from stayapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('product', views.product),
    path('about', views.about),
    path('register', views.register), 
    path('city/<cid>', views.city),
    path('search', views.search),
    path("login", views.user_login),
    path('logout', views.user_logout),
    path('index', views.index),
    path('contact', views.contact),
    path('sort/<sid>', views.sort),
    path('products/<pid>', views.products),
    path('pricefilter', views.pricefilter),
    path('addtocart/<pid>', views.addtocart),
    path('cart', views.cart),
    path('remove/<cid>', views.remove),
    path('updateqty/<x>/<cid>', views.updateqty),
    path('makepayment', views.makepayment),
    path('place_order', views.placeorder),
    path('fetchorder', views.fetchorder),
    path('paymentsuccess', views.paymentsuccess),
    path('orderhistory', views.orderhistory),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)