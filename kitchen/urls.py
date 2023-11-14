from django.urls import path

from kitchen.views import index, CookListView, DishListView, DishTypeListView, DishDetailView, CookCreateView

urlpatterns = [
    path("", index, name="index"),
    path("cooks/", CookListView.as_view(), name="cook-list"),
    path("menu/", DishListView.as_view(), name="menu"),
    path("drinks_menu/", DishListView.as_view(), name="drinks-menu"),
    path("dish_types/", DishTypeListView.as_view(), name="dish-type=list"),
    path("dish_detail/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("create_cooks/", CookCreateView.as_view(), name="create-cooks"),

]


app_name = "kitchen"
