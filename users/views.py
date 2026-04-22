from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import FormView, UpdateView
from .forms import ProfileForm, RegisterForm


def _style_auth_form(form):
    # This helper injects ui classes into AuthenticationForm fields.
    for field in form.fields.values():
        field.widget.attrs["class"] = "form-control"

class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, _("Cuenta creada correctamente"))
        return super().form_valid(form)


class LoginView(View):
    template_name = "users/login.html"

    def get(self, request):
        form = AuthenticationForm()
        _style_auth_form(form)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        _style_auth_form(form)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, _("Sesión iniciada correctamente"))
            return redirect("core:home")
        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.info(request, _("Sesión cerrada"))
        return redirect("core:home")


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = "users/profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, _("Perfil actualizado"))
        return super().form_valid(form)
