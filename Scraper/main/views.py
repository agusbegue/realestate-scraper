from django.views.generic import FormView, View, ListView, DetailView
from django.shortcuts import get_object_or_404, render, redirect
from requests.exceptions import ConnectionError as ReqConnectionError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse

import io
from scrapyd_api import ScrapydAPI
from xlsxwriter.workbook import Workbook

from main.models import ScrapyJob, Property, Statistics
from main.forms import JobForm
from main.excel import FileCreator


class Index(LoginRequiredMixin, ListView, FormView):

    template_name = 'index.html'
    model = ScrapyJob
    form_class = JobForm
    success_url = '/'

    def get_queryset(self):
        return ScrapyJob.objects.filter(user=self.request.user)

    def form_valid(self, form):
        job = ScrapyJob(user=self.request.user)
        job.start(form.files['file'])
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class Properties(LoginRequiredMixin, View):

    template = 'properties.html'

    def get(self, request):
        if request.GET.get('job_id'):
            job = ScrapyJob.objects.select_related('user').get(pk=request.GET.get('job_id'))
            if not job or job.user != request.user:
                return render(request, 'error/404.html')
            properties = Property.objects.filter(job=job)
        else:
            properties = Property.objects.filter(job__user=request.user)
        return render(request, self.template, {'properties': properties})


class StatisticsView(DetailView):

    model = Statistics
    template_name = 'statistics.html'


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


class OptionsHandlerView(LoginRequiredMixin, View):
    error_404 = 'error/404.html'
    error_500 = 'error/500.html'


class JobOptionsHandlerView(OptionsHandlerView):

    def get(self, request, action, job_id):
        if action == 'download':
            job = ScrapyJob.objects.select_related('user').get(id=job_id)
            if job and job.user == request.user:
                response = HttpResponse(job.to_file(),
                                        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                response['Content-Disposition'] = "attachment; filename=job-{}.xlsx".format(job_id)
                return response
        return render(request, self.error_404)

    def post(self, request, action, job_id):
        if action == 'delete':
            job = ScrapyJob.objects.select_related('user').get(id=job_id)
            if job and job.user == request.user:
                job.cancel()
                job.delete()
                return JsonResponse({'status': 'success'})
        return render(request, self.error_404)


class PropertyOptionsHandlerView(OptionsHandlerView):

    def get(self, request, action, prop_id):
        if action == 'download':
            prop = Property.objects.select_related('job__user').get(id=prop_id)
            if prop and prop.job.user == request.user:
                response = HttpResponse(prop.to_file(),
                                        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                response['Content-Disposition'] = "attachment; filename=property-{}.xlsx".format(prop_id)
                return response
        return render(request, self.error_404)

    def post(self, request, action, prop_id):
        if action == 'delete':
            prop = Property.objects.select_related('job__user').get(id=prop_id)
            if prop and prop.job.user == request.user:
                # ver que onda cuando vuelve la propiedad si no esta done
                prop.delete()
                return JsonResponse({'status': 'success'})
        return render(request, self.error_404)


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
