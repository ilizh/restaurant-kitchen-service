from django.urls import path

from kitchen.views import index, CookListView, DishListView, DishTypeListView, DishDetailView, CookCreateView, \
    UserLogoutView, UserLoginView, DishCreateView, toggle_assign_to_dish, DishTypeCreateView

urlpatterns = [
    path("", index, name="index"),
    path("cooks/", CookListView.as_view(), name="cook-list"),
    path("menu/", DishListView.as_view(), name="menu"),
    path("dish_types/", DishTypeListView.as_view(), name="dish-types"),
    path("dish_detail/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("cooks/create_cooks/", CookCreateView.as_view(), name="create-cooks"),
    path("menu/create_dish/", DishCreateView.as_view(), name="create-dish"),
    path("dish_types/create_dishtype/", DishTypeCreateView.as_view(), name="create-dish-type"),
    path(
        "menu/<int:pk>/toggle-assign/",
        toggle_assign_to_dish,
        name="toggle-dish-assign",
    ),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("logout/", UserLogoutView.as_view(), name="user-logout"),
]
app_name = "kitchen"
