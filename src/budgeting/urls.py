from django.urls import path, include
from . import views

app_name = 'budgeting'


urlpatterns = [
    path("",views.Budgeting.as_view(), name='budgeting_page' ),
    path("add-expences",views.AddExpenses.as_view(), name='add_expences' ),
    path("update-expences/<int:pk>",views.UpdateExpenses.as_view(), name='update_expences' ),
    path("detail-expences/<int:pk>",views.DetailExpenses.as_view(), name='detail_expences' ),
]

