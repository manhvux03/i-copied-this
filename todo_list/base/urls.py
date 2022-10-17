from django.urls import path
from .views import RegisterPage, TaskList,  TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, RegisterPage
# do views nayf cungf file với urls nên có thể làm vậy để làm đẹp web etc
#thực ra chúng ta có thể import luôn nhưng ở bên views viets 1 lần để biết nó 
#hoạt động ra sao
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(next_page='login'), name = 'logout'),
    path('register/',RegisterPage.as_view(), name = 'register' ),
    #theo suffix của logout thì chúng ta để thêm next_page 
    path('',TaskList.as_view(), name='tasks'),
    path('task/<int:pk>',TaskDetail.as_view(), name='task'),
    #sau khi import detail view trong view
    path('task-create/',TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>',TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>',TaskDelete.as_view(), name='task-delete'),
]  