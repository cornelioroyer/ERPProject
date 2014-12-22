__author__ = 'FARID ILHAM Al-Q'

from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.urlresolvers import reverse
from django.contrib.auth.tokens import default_token_generator
from django.template.response import TemplateResponse
from django.utils.http import base36_to_int
from django.conf import settings
from django.shortcuts import resolve_url
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from Apps.Distribution.customer.forms import RegistrationForm, LoginForm, UpdateForm
from Apps.Distribution.customer.models import Company


def registration(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/profile')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password1'],

                                            )
            user.is_active = False
            user.save()
            company = Company(user=user, name=form.cleaned_data['name'],
                              corporate=form.cleaned_data['corporate'],
                              email=form.cleaned_data['email'],
                              industry=form.cleaned_data['industry'],
                              business=form.cleaned_data['business'],
                              zip_code=form.cleaned_data['zip_code'],
                              country=form.cleaned_data['country'],
                              address=form.cleaned_data['address'],
                              phone=form.cleaned_data['phone'],
                              type=form.cleaned_data['type'],
                              currency=form.cleaned_data['currency'],
                              position=form.cleaned_data['position'],
            )
            company.save()
            return HttpResponseRedirect('/accounts/success')
        else:
            return render_to_response('registration/register.html', {'form': form},
                                      context_instance=RequestContext(request))
    else:
        form = RegistrationForm()
        context = {'form': form, }
        return render_to_response('registration/register.html', context, context_instance=RequestContext(request))


def registration_success(request):
    return render_to_response('registration/register_success.html', context_instance=RequestContext(request))


def username_change(request):
    return render_to_response('registration/username_change.html', context_instance=RequestContext(request))


def login_request(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/profile/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            company = authenticate(username=username, password=password)

            if company is not None:
                login(request, company)
                return HttpResponseRedirect('/accounts/profile/')
            else:
                return render_to_response('registration/login.html', {'form': form},
                                          context_instance=RequestContext(request))
        else:
            return render_to_response('registration/login.html', {'form': form},
                                      context_instance=RequestContext(request))
    else:
        form = LoginForm()
        context = {'form': form}
        return render_to_response('registration/login.html', context, context_instance=RequestContext(request))


def password_reset(request, is_admin_site=False,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('django.contrib.auth.views.password_reset_done')
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
            }
            if is_admin_site:
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def password_reset_done(request,
                        template_name='registration/password_reset_done.html',
                        current_app=None, extra_context=None):
    context = {}
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


@sensitive_post_parameters()
@never_cache
def password_reset_confirm(request, uidb36=None, token=None,
                           template_name='registration/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           current_app=None, extra_context=None):

    UserModel = get_user_model()
    assert uidb36 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('django.contrib.auth.views.password_reset_complete')
    try:
        uid_int = base36_to_int(uidb36)
        user = UserModel._default_manager.get(pk=uid_int)
    except (ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(None)
    else:
        validlink = False
        form = None
    context = {
        'form': form,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def password_reset_complete(request,
                            template_name='registration/password_reset_complete.html',
                            current_app=None, extra_context=None):
    context = {
        'login_url': resolve_url(settings.LOGIN_URL)
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request,
                    template_name='registration/password_change_form.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    current_app=None, extra_context=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('password_change_done')
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


@login_required
def password_change_done(request,
                         template_name='registration/password_change_done.html',
                         current_app=None, extra_context=None):
    context = {}
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def logout_request(request):
    logout(request)
    return HttpResponseRedirect('/accounts/logged_out')


def logout_success(request):
    return render_to_response('registration/logout.html', context_instance=RequestContext(request))


@login_required
def profile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    company = request.user.get_profile
    context = {'company': company}
    return render_to_response('registration/profile.html', context, context_instance=RequestContext(request))


@login_required
def update_profile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    profiles = request.user.get_profile()
    if request.method == 'POST':
        form = UpdateForm(request.POST, request.FILES, instance=profiles)
        if form.is_valid():
            human = True
            form.save()
            return HttpResponseRedirect('/accounts/profile')
        else:
            return render_to_response('registration/update_profile.html', {'form': form},context_instance=RequestContext(request))

    else:
        form = UpdateForm(instance=profiles)
        context = {'form': form, }

    return render_to_response('registration/update_profile.html', context, context_instance=RequestContext(request))



