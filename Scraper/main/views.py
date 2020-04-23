import json

from uuid import uuid4
from urllib.parse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse
from scrapyd_api import ScrapydAPI
# from main.utils import URLUtil
from django.views import generic
from requests.exceptions import ConnectionError as ReqConnectionError
import socket

from main.models import Post, ScrapyJob
from main.options import categorias, lugares

home_context = {'categorias': categorias.keys(), 'lugares': lugares}

@csrf_exempt
def crawl(request):
    try:
        Post.objects.all().delete()

        job = ScrapyJob('http://localhost:6800')
        categoria = categorias[request.POST['categoria']]
        lugar = lugares[request.POST['lugar']]
        job.start(categoria, lugar)
        context = {'task_id': job.task, 'status': job.status,
                   'host': str(socket.gethostbyname(socket.gethostname()))}
        # return redirect(reverse('loading', args=[context]))
        return render(request, 'main/loading.html', context)
    except KeyError:
        return render(request, 'main/home.html', {'error_message': 'Selecciona una opcion pa', **home_context})
    except ReqConnectionError:
        #return redirect(reverse('error', kwargs={'details': 'Unable to connect to Scrapy API'}))
        return render(request, 'main/error.html', {'details': 'Unable to connect to Scrapy API'})
    except Exception as e:
        return render(request, 'main/error.html', {'details': str(e)})


def home(request):
    return render(request, 'main/home.html', {'posts': len(Post.objects.all()), **home_context})


def finished(request, context):
    return render(request, 'main/finished.html', context)


def error(request, context):
    return render(request, 'main/error.html', context)


def loading(request, context):
    return render(request, 'main/loading.html', context)

#def crawl_finished(request):
    #context

#@method_decorator(csrf_exempt, name='dispatch')
class ListView(generic.ListView):
    template_name = 'main/list.html'

    def get_queryset(self):
        """Return the last five published posts."""
        return Post.objects.all()


class DetailView(generic.DetailView):
    model = Post
    template_name = 'main/detail.html'


def get_lugares(request):
    return JsonResponse([{'id': i, 'text': val} for i, val in enumerate(lugares.keys())], safe=False)

# @csrf_exempt
# @require_http_methods(['POST', 'GET'])  # only get and post
# def crawl(request):
#     # Post requests are for new crawling tasks
#     if request.method == 'POST':
#
#         url = request.POST.get('url', None)  # take url comes from client. (From an input may be?)
#
#         if not url:
#             return JsonResponse({'error': 'Missing  args'})
#
#         if not is_valid_url(url):
#             return JsonResponse({'error': 'URL is invalid'})
#
#         domain = urlparse(url).netloc  # parse the url and extract the domain
#         unique_id = str(uuid4())  # create a unique ID.
#
#         # This is the custom settings for scrapy spider.
#         # We can send anything we want to use it inside spiders and pipelines.
#         # I mean, anything
#         settings = {
#             'unique_id': unique_id,  # unique ID for each record for DB
#             'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
#         }
#
#         # Here we schedule a new crawling task from scrapyd.
#         # Notice that settings is a special argument name.
#         # But we can pass other arguments, though.
#         # This returns a ID which belongs and will be belong to this task
#         # We are goint to use that to check task's status.
#         task = scrapyd.schedule('default', 'idealista',
#                                 settings=settings, url=url, domain=domain)
#
#         return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started'})
#
#     # Get requests are for getting result of a specific crawling task
#     elif request.method == 'GET':
#         # We were passed these from past request above. Remember ?
#         # They were trying to survive in client side.
#         # Now they are here again, thankfully. <3
#         # We passed them back to here to check the status of crawling
#         # And if crawling is completed, we respond back with a crawled data.
#         task_id = request.GET.get('task_id', None)
#         unique_id = request.GET.get('unique_id', None)
#
#         if not task_id or not unique_id:
#             return JsonResponse({'error': 'Missing args'})
#
#         # Here we check status of crawling that just started a few seconds ago.
#         # If it is finished, we can query from database and get results
#         # If it is not finished we can return active status
#         # Possible results are -> pending, running, finished
#         status = scrapyd.job_status('default', task_id)
#         if status == 'finished':
#             try:
#                 # this is the unique_id that we created even before crawling started.
#                 item = ScrapyItem.objects.get(unique_id=unique_id)
#                 return JsonResponse({'data': item.to_dict['data']})
#             except Exception as e:
#                 return JsonResponse({'error': str(e)})
#         else:
#             return JsonResponse({'status': status})
# def is_valid_url(url):
#     validate = URLValidator()
#     try:
#         validate(url)  # check if url format is valid
#     except ValidationError:
#         return False
#
#     return True
