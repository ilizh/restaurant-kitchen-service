from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView
from kitchen.forms import DishSearchForm, CookCreationForm, DishCreationForm, DishTypeForm

from kitchen.models import DishType, Dish, Cook


# Create your views here.
def index(request):
    dish_type = DishType.objects.all()

    context = {
        "dish_type": dish_type
    }
    return render(request, "kitchen/index.html", context=context)


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    context_object_name = "dish_types"
    template_name = "kitchen/dish_types.html"
    paginate_by = 10


class DishTypeDetailView(generic.DetailView):
    model = DishType


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    paginate_by = 5


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm
    success_url = reverse_lazy("kitchen:cook-list")


class CookDetailView(generic.DetailView):
    model = Cook


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 3
    template_name = "kitchen/menu.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(
            initial={"name": name}
        )
        return context


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishCreationForm
    success_url = reverse_lazy("kitchen:menu")


class DishDetailView(generic.DetailView):
    model = Dish
    queryset = Dish.objects.select_related('dish_type').prefetch_related('cooks')


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    form_class = DishTypeForm
    success_url = reverse_lazy("kitchen:dish-types")


class UserLoginView(LoginView):
    template_name = "registration/login.html"
    success_url = reverse_lazy("kitchen:index")


class UserLogoutView(LogoutView):
    template_name = "registration/register.html"
    success_url = reverse_lazy("kitchen:index")


@login_required
def toggle_assign_to_dish(request, pk):
    cook = Cook.objects.get(id=request.user.id)
    dish = Dish.objects.get(id=pk)

    if dish in cook.dishes.all():
        cook.dishes.remove(dish)
    else:
        if dish in Dish.objects.filter(cooks=cook):
            cook.dishes.add(dish)
    return HttpResponseRedirect(reverse_lazy("kitchen:dish-detail", args=[pk]))
