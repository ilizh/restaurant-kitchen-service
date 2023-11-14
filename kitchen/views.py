from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from kitchen.forms import DishTypeSearchForm, DishSearchForm, CookCreationForm
from kitchen.models import DishType, Dish, Cook


<<<<<<< HEAD
=======
# Create your views here.
>>>>>>> 000f36bf908d2fc4fe0b31e684013693c82dd3bf
def index(request):
    dish_type = DishType.objects.all()

    context = {
        "dish_type": dish_type
    }
    return render(request, "kitchen/index.html", context=context)


class DishTypeListView(generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "kitchen/dish_type_list.html"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishTypeListView(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = DishType.objects.all()
        form = DishTypeSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class DishTypeDetailView(generic.DetailView):
    model = DishType


class CookListView(generic.ListView):
    model = Cook
    paginate_by = 10


<<<<<<< HEAD
class CookCreateView(LoginRequiredMixin, generic.CreateView):
=======
class CookDetailView(generic.DetailView):
>>>>>>> 000f36bf908d2fc4fe0b31e684013693c82dd3bf
    model = Cook
    form_class = CookCreationForm


class DishListView(generic.ListView):
    model = Dish
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishListView(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Dish.objects.prefetch_related('cooks')
        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class DishDetailView(generic.DetailView):
    model = Dish
    queryset = Dish.objects.select_related('dish_type').prefetch_related('cooks')
