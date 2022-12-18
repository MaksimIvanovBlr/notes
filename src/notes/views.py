from django.shortcuts import render
from . import models, forms
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class NotesView(generic.TemplateView):
    template_name = "notes/main.html"




class  CreateNote(generic.CreateView):
    model = models.Notes
    form_class = forms.NotesForm
    template_name = "notes/edit_note.html"
    success_url = reverse_lazy('notes:main')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Создать заметку'
        return context
    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)

class UpdateNote(generic.UpdateView):
    model = models.Notes
    template_name = "notes/edit_note.html"
    success_url = reverse_lazy('notes:main')
    form_class = forms.NotesForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Изменить заметку'
        return context

class ListNote(generic.ListView):
    model = models.Notes
    template_name = "notes/list_note.html"
    def get_queryset(self):
        user = self.request.user
        object_list = models.Notes.objects.filter(user=user)
        return object_list

class DetailNote(generic.DetailView):
    model = models.Notes
    template_name = "notes/detail.html"

class DeleteNote(generic.DeleteView):
    model = models.Notes
    template_name = "notes/delete_note.html"
