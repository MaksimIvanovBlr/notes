from django.urls import path
from . import views

app_name = 'notes'


urlpatterns = [
    path("",views.NotesView.as_view(), name='main' ),
    path("create/",views.CreateNote.as_view(), name='create' ),
    path("update/<int:pk>",views.UpdateNote.as_view(), name='update' ),
    path("list",views.ListNote.as_view(), name='list' ),
    path("delete/<int:pk>",views.DeleteNote.as_view(), name='delete' ),
    path("detail/<int:pk>",views.DetailNote.as_view(), name='detail' ),
]

