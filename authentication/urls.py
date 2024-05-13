from django.urls import path


from .views  import CreateUserView

urlpatterns = [
    # path('login', views.login ),
    path("register/", CreateUserView.as_view(), name="register" ),

]