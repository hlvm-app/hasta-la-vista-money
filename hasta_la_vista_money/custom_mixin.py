from typing import Optional

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView
from hasta_la_vista_money.constants import MessageOnSite


class CustomNoPermissionMixin(LoginRequiredMixin):
    no_permission_url = None
    permission_denied_message = ''
    redirect_field_name = ''
    request = ''

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(self.no_permission_url)


class DeleteCategoryMixin(DeleteView):
    model = Optional[None]
    success_url = None

    def form_valid(self, form):
        try:
            category = self.object
            category.delete()
            messages.success(
                self.request,
                MessageOnSite.SUCCESS_CATEGORY_DELETED.value,
            )
            return super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                MessageOnSite.ACCESS_DENIED_DELETE_CATEGORY.value,
            )
            return redirect(self.success_url)


class CustomSuccessURLUserMixin:
    def __init__(self):
        """Конструктов класса инициализирующий аргумент kwargs."""
        self.kwargs = None

    def get_success_url(self):
        user = self.kwargs['pk']
        return reverse_lazy('users:profile', kwargs={'pk': user})


class ExpenseIncomeFormValidCreateMixin(CreateView):
    model = None
    form_class = None

    def __init__(self, *args, **kwargs):
        """
        Конструктов класса инициализирующий аргументы класса.

        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.request = None

    def post(self, request, *args, **kwargs):
        category_name = request.POST.get('name')
        categories = self.model.objects.filter(
            user=request.user,
            name=category_name,
        )

        add_category_form = self.form_class(request.POST)

        if categories:
            messages.error(
                request,
                f'Категория "{category_name}" уже существует!',
            )
            return redirect(self.success_url)
        elif add_category_form.is_valid():
            category_form = add_category_form.save(commit=False)
            category_form.user = request.user
            category_form.save()
            messages.success(
                request,
                f'Категория "{category_name}" была успешно добавлена!',
            )
            return redirect(self.success_url)
        messages.error(
            request,
            f'Категория "{category_name}" не может быть добавлена!',
        )
        return redirect(self.success_url)


class UpdateViewMixin:
    def __init__(self):
        """Конструктов класса инициализирующий аргументы класса."""
        self.template_name = None
        self.request = None

    def get_update_form(self, form_class=None, form_name=None):
        model = self.get_object()
        form = form_class(instance=model)
        return render(
            self.request,
            self.template_name,
            {form_name: form},
        )
