from django.shortcuts import render
from django.views import generic

from kitchen.models import DishType, Dish, Cook


# Create your views here.
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


class DishTypeDetailView(generic.DetailView):
    model = DishType


class CookListView(generic.ListView):
    model = Cook
    paginate_by = 10


class CookDetailView(generic.DetailView):
    model = Cook


class DishListView(generic.ListView):
    model = Dish
    paginate_by = 10
    queryset = Dish.objects.prefetch_related('cooks')


class DishDetailView(generic.DetailView):
    model = Dish
    queryset = Dish.objects.select_related('dish_type').prefetch_related('cooks')
