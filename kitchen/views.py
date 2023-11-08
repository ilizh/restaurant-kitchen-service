from django.shortcuts import render
from django.views import generic

from kitchen.models import DishType, Dish, Cook


# Create your views here.
# а это хз зачем, потом решу куда его совать, можно сделать как регистрационную страницу +-
def index(request):
    dish_type = DishType.objects.all()

    context = {
        "dish_type": dish_type
    }
    return render(request, "kitchen/index.html", context=context)


# тут сделать список из всех видов блюд + их кол-во
class DishTypeListView(generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "kitchen/dish_type_list.html"
    paginate_by = 10


# тут детали , тут понятно все
class DishTypeDetailView(generic.DetailView):
    model = DishType


# список всех шефов и их года экспириенса
class CookListView(generic.ListView):
    model = Cook
    paginate_by = 10


# тут детали шефа, я думаю понятно
class CookDetailView(generic.DetailView):
    model = Cook


# список из всех блюд, их вид, их прайс
class DishListView(generic.ListView):
    model = Dish
    paginate_by = 10
    queryset = Dish.objects.prefetch_related('cooks')


# тут детали блюда, цена, название, описание, возможно время приготовления
class DishDetailView(generic.DetailView):
    model = Dish
    queryset = Dish.objects.select_related('dish_type').prefetch_related('cooks')

# завтра доделать вьюшки, сёрч формы, регистрацию +-, темплейты и если будет время их кастомизировать через бутстрап
