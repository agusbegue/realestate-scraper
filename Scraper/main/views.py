from django.views.generic import FormView, View, ListView
from django.shortcuts import get_object_or_404, render, redirect
from requests.exceptions import ConnectionError as ReqConnectionError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from scrapyd_api import ScrapydAPI

from main.models import ScrapyJob, Property
from main.forms import JobForm


class Index(LoginRequiredMixin, ListView, FormView):

    template_name = 'index.html'
    model = ScrapyJob
    form_class = JobForm
    success_url = ''

    def get_queryset(self):
        return ScrapyJob.objects.filter(user=self.request.user)

    def form_valid(self, form):
        # job = ScrapyJob(user=self.request.user)
        # job.start(form.files['file'])
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class OptionsHandlerView(View):

    def post(self, request, action, job_id):
        # ver que onda cuando esta running o pending
        if action == 'delete':
            ScrapyJob.objects.filter(id=job_id).delete()
            return JsonResponse({'status': 'success'})
        elif action == 'download':
            pass
        return JsonResponse({'status': 'error'})


class Properties(LoginRequiredMixin, View):

    template = 'properties.html'

    def get(self, request):
        if request.GET.get('job_id'):
            job = ScrapyJob.objects.get(pk=request.GET.get('job_id'))
            if not job:
                return 404
            if job.user != request.user:
                return 401
            properties = Property.objects.filter(job=job)
        else:
            properties = Property.objects.filter(job__user=request.user)
        return render(request, self.template, {'properties': properties})


class Login(View):
    template = 'auth/login.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, self.template, {'form': form, 'error_message': 'Wrong email or password'})


class ChangePassword(PasswordChangeView):

    template_name = 'auth/password.html'
    success_url = ''




'''
class PropertyView(DetailView):
    model = Property
    template_name = 'main/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # validar que ese usuario puede ver esa prop
        context['property'] = get_object_or_404(Property, pk=kwargs['id'])
        return context
'''
