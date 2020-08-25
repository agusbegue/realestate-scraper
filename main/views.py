from django.views.generic import FormView, View, ListView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.db.models import Prefetch

from main.models import ScrapyJob, Property
from main.forms import JobForm


class Index(LoginRequiredMixin, ListView, FormView):

    template_name = 'index.html'
    model = ScrapyJob
    form_class = JobForm
    success_url = '/'

    def get_queryset(self):
        ## ver que onda las running
        return ScrapyJob.objects.filter(user=self.request.user)

    def form_valid(self, form):
        job = ScrapyJob(user=self.request.user)
        job.start(form.files['file'])
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class Properties(LoginRequiredMixin, View):

    template = 'propertys.html'

    def get(self, request):
        if request.GET.get('job_id'):
            job = ScrapyJob.objects.select_related('user').prefetch_related(Prefetch('property_set__post_set'))\
                                   .get(pk=request.GET['job_id'])
            if not job or job.user != request.user:
                return render(request, 'error/404.html')
            propertys = job.property_set.all()
        else:
            propertys = Property.objects.filter(job__user=request.user).prefetch_related('post_set')
        return render(request, self.template, {'propertys': [{'prop': prop, 'posts': prop.post_set.all()} for prop in propertys]})


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


class JobOptionsHandlerView(LoginRequiredMixin, View):
    error_404 = 'error/404.html'
    error_500 = 'error/500.html'

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
                job.delete()
                return JsonResponse({'status': 'success'})
        return render(request, self.error_404)


class PropertyOptionsHandlerView(LoginRequiredMixin, View):
    error_404 = 'error/404.html'
    error_500 = 'error/500.html'

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

