from django.shortcuts import render
# from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
#make a detail view from an item
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
#những fuction import từ cùng nguồn thì dùng chung một file template
#vd như 2 cái trên dùng chung task_list
from django.urls import reverse_lazy
# khi mà các dòng lệnh đc chạy, để đảm bảo user tới được đúng nơi của web
#thì chúng ta dùng cái này 
from django.contrib.auth.views import LoginView
#build-in fuction django đã chuẩn bị sẵn

from django.contrib.auth.mixins import LoginRequiredMixin
#để truy cập đc thông tin thì cần phải login

#dungf built-in form đã có sẵn -FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields= '__all__'
    redirect_authenticated_user = True
    #do index của red_auth_user là false nên sửa lại

    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        user=form.save()
        if user is not None:
            login(self.request, user)
        #nếu user reg thành công thì tự login cho họ
        return super(RegisterPage, self).form_valid(form)





# def taskList(request):
#     return HttpResponse('To Do List')
# de thu? xem web co hoat dong k, co thi se return todolist


# def productsList(request):
# 	products = Product.objects.all()
	
# 	if request.method == 'POST':
#   		Product.object.create()
	
# 	context = {'products':products}
# 	return render(request, 'base/product_list.html', context)
# nếu req method = post tức là người dùng nhập dữ liệu
#thì tạo một object mới ở product với key là tên, value là product 
# rồi chạy trên web/ render trên web thêm một product trong product list

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
    #passing in/ cho vào các dữ liệu ban đầu/ keyword arguments
    #kwargs là các giá trị mà khi nó đi vào fuction, 
    #nó được nhận dạng bởi các biến xác định, 
    #tức là giá trị của kwargs không thay đổi xuyên suốt fuction
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        #make sure that user can only acess to their own data
        context['count'] = context['tasks'].filter(complete=False).count()
        #thêm vào cho vui, đếm số item chưa 'complete' 


        search_input = self.request.GET.get('search-area')or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        
        context['search_input'] = search_input
        return context
    


#sau khi add thêm mix-in thì khi vào tab, nó sẽ tự động dẫn bạn tới login
class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name= 'task'
    template_name = 'base/task.html'
#tức là gọi ra task template của base, thực hiện code trong đó 
class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    # View for creating a new object, with a response rendered by a template.
    fields = ['title','description','complete']
    #ban đầu thì có cả dòng chọn user để add task
    #nhưng chugns ta k cần nữa nên bỏ nó đi
    success_url = reverse_lazy('tasks')
    #tức là sau khi tạo một item mới thì gửi user về list item

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    #giờ chúng ta muốn xóa thì cần 2 bước,
    #bước 1 là hỏi xem có chắc chắn muốn xóa k
    #nếu muốn thì thực hiện bước 2 là xóa

# class BaseDeleteView(DeletionMixin, FormMixin, BaseDetailView):
#     """
#     Base view for deleting an object.
#     Using this base class requires subclassing to provide a response mixin.
#     """

#     form_class = Form

#     def __init__(self, *args, **kwargs):
#         if self.__class__.delete is not DeletionMixin.delete:
#             warnings.warn(
#                 f"DeleteView uses FormMixin to handle POST requests. As a "
#                 f"consequence, any custom deletion logic in "
#                 f"{self.__class__.__name__}.delete() handler should be moved "
#                 f"to form_valid().",
#                 DeleteViewCustomDeleteWarning,
#                 stacklevel=2,
#             )
#         super().__init__(*args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         # Set self.object before the usual form processing flow.
#         # Inlined because having DeletionMixin as the first base, for
#         # get_success_url(), makes leveraging super() with ProcessFormView
#         # overly complex.
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

#     def form_valid(self, form):
#         success_url = self.get_success_url()
#         self.object.delete()
#         return HttpResponseRedirect(success_url)