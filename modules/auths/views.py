from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe

from core.decorators import owner_or_role_required, owner_required

from .forms import AccountForm, AccountPasswordForm, LoginForm
from .models import Account, StatusAccount

# Create your views here.


def logout_app(request):
    logout(request)
    return redirect("home")


def login_app(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is None:
                messages.error(request, "Error en las credenciales")
                return render(request, "login.html", {"form": form})
            else:
                account = Account.getAccount(user)
                login(request, user)
                messages.success(request, f"Bienvenido {account.fullname}")
                return redirect("sendInvoice")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


@owner_required
def users_list(request):
    users = Account.objects.all()
    return render(request, "user_list.html", {"users": users})


@owner_required
def user_create(request):
    account = Account.getAccount(request.user)
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            try:
                status = StatusAccount.objects.get(pk=1)
            except StatusAccount.DoesNotExist:
                return render(request, "user_create.html", {"form": form})
            user.created_by = account.username
            user.status = status
            user.save()
            form.save_m2m()
            request.session["new_account_id"] = user.id
            return redirect("user_assign_password")
        else:
            print(form.errors)
    else:
        form = AccountForm()
    return render(request, "user_create.html", {"form": form})


@owner_or_role_required("Admin")
def assign_password(request):
    if request.session.get("new_account_id"):
        account_id = request.session.get("new_account_id")
        if not account_id:
            messages.error(request, "Primero completa los datos del usuario.")
            return redirect("account_create_step1")

        account = Account.objects.get(id=account_id)

        if request.method == "POST":
            form = AccountPasswordForm(account, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Usuario creado exitosamente.")
                del request.session["new_account_id"]
                return redirect("users_list")
            else:
                errors = None
                for field, field_errors in form.errors.items():
                    for error in field_errors:
                        if errors is None:
                            errors = f"{error}<br>"
                        else:
                            errors += f"{error}<br>"
                messages.error(request, mark_safe(errors))
        else:
            form = AccountPasswordForm(account)

        return render(
            request, "user_password.html", {"form": form, "account": account, "change": False}
        )
    else:
        account = Account.getAccount(request.user)
        if request.method == "POST":
            form = AccountPasswordForm(account, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Contraseña actualizada correctamente.")
                return redirect("sendInvoice")
            else:
                errors = None
                for field, field_errors in form.errors.items():
                    for error in field_errors:
                        if errors is None:
                            errors = f"{error}<br>"
                        else:
                            errors += f"{error}<br>"
                messages.error(request, mark_safe(errors))
        else:
            form = AccountPasswordForm(account)

        return render(
            request, "user_password.html", {"form": form, "account": account, "change": True}
        )


@owner_required
def user_update(request, user_id):
    account = Account.getAccount(request.user)
    try:
        user = Account.objects.get(id=user_id)
    except Account.DoesNotExist:
        messages.error(request, "El usuario no existe.")
        return redirect("users_list")

    if request.method == "POST":
        form = AccountForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.updated_by = account.username
            user.save()
            messages.success(request, "Usuario actualizado exitosamente.")
            return redirect("users_list")
        else:
            print(form.errors)
    else:
        form = AccountForm(instance=user)

    return render(request, "user_update.html", {"form": form, "user": user})


@owner_required
def user_query(request, user_id):
    try:
        user = Account.objects.get(id=user_id)
    except Account.DoesNotExist:
        messages.error(request, "El usuario no existe.")
        return redirect("users_list")

    form = AccountForm(instance=user)
    for field in form.fields.values():
        field.disabled = True

    return render(request, "user_query.html", {"form": form, "user": user})
