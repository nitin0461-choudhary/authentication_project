from django.urls import path
from student.views import  home,register, reg_success, new_login, thanks, work_board,forget_password

urlpatterns = [
    path('', home, name="home"),
    path('register/', register, name="register"),
    path('success/', reg_success, name="reg_success"),
    path('new_login/', new_login, name="new_login"),
    path('thanks/', thanks, name="thanks"),
    path('work-board/', work_board, name="work_board"),
    path('forget_password/',forget_password,name="forget_password")

]
