from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.views.generic import FormView, CreateView
from django.views.generic.detail import SingleObjectMixin
User = get_user_model()

from .forms import ExistingListItemForm, ItemForm, NewListForm
from .models import List


class HomePageView(FormView):
    form_class = ItemForm
    template_name = 'home.html'


class NewListView(CreateView):
    form_class = ItemForm
    template_name = 'home.html'


    def post(self, request):
        return redirect(form.save(owner=request.user))


class ViewAndAddToList(CreateView, SingleObjectMixin):
    template_name = 'list.html'
    model = List
    form_class = ExistingListItemForm

    def get_form(self, form_class):
        self.object = self.get_object()
        return form_class(for_list=self.object, data=self.request.POST)


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def new_list(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request, 'home.html', {'form': form})

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)

    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)

    if form.is_valid():
        form.save()
        return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})


def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})


def share_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    list_.shared_with.add(request.POST['email'])
    return redirect(list_)
