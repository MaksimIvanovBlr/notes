from django.shortcuts import render
from . import models, forms
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from expences.date_day_to import date


class NotesView(LoginRequiredMixin, generic.TemplateView):
    template_name = "notes/main.html"
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = models.Notes.objects.filter(
            Q(user=self.request.user) & Q(update_date__year=date.year, update_date__month=date.month))
        return context


class CreateNote(LoginRequiredMixin, generic.CreateView):
    model = models.Notes
    form_class = forms.NotesForm
    template_name = "notes/edit_note.html"
    success_url = reverse_lazy('notes:main')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Создать заметку'
        return context

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)


class UpdateNote(LoginRequiredMixin, generic.UpdateView):
    model = models.Notes
    template_name = "notes/edit_note.html"
    success_url = reverse_lazy('notes:main')
    login_url = reverse_lazy('login')
    form_class = forms.NotesForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Изменить заметку'
        return context


class ListNote(LoginRequiredMixin, generic.ListView):
    model = models.Notes
    template_name = "notes/list_note.html"
    login_url = reverse_lazy('login')

    def get_queryset(self):
        user = self.request.user
        object_list = models.Notes.objects.filter(user=user)
        return object_list


class DetailNote(LoginRequiredMixin, generic.DetailView):
    model = models.Notes
    template_name = "notes/detail_note.html"
    login_url = reverse_lazy('login')


class DeleteNote(LoginRequiredMixin, generic.DeleteView):
    model = models.Notes
    template_name = "notes/delete_note.html"
    success_url = reverse_lazy('notes:main')
    login_url = reverse_lazy('login')
