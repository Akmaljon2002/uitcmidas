from django.urls import path
from admins.views import get_users, user_delete, AdminCategoriesView, AdminCategoryDetailView

urlpatterns = [
    path('users/', get_users, name='get_users'),
    path('user/delete/<int:pk>', user_delete, name='delete_user'),

    path('categories/', AdminCategoriesView.as_view(), name='categories_admin'),
    path('category/<int:pk>/', AdminCategoryDetailView.as_view(), name='category_admin'),

]
