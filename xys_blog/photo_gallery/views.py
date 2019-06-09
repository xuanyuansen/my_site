from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db import models
from .forms import ImageForm
from .models import Image
# Create your views here.


def gallery(request):
    image_list = Image.objects.all()
    for star in image_list.iterator():
        print("object is", star)
        print("url is", star.url)
        print("title is", star.title)
        print("slug is", star.slug)
        print("image is ", star.image)
        print("user is ", star.user)
        print("created is", star.created)

    return render(request, 'gallery/index.html', {
        'image_list': image_list
        })


@login_required(login_url='/userprofile/login/')
@csrf_exempt
@require_POST
def upload_image(request):
    print("request", request.POST)
    file_obj = request.FILES.get('file')
    print(type(file_obj))
    if file_obj is not None:
        data = request.POST
        title = data.get('title')
        description = data.get('description')
        print(title, description)
        print(request.user)
        image = Image(title=title, image=file_obj, description=description, user=request.user)
        print(image, "type of image", type(image))
        image.save()
        print("file is", file_obj)
        return JsonResponse({'status': "1"})

    form = ImageForm(data=request.POST)
    if form.is_valid():
        try:
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            return JsonResponse({'status': "1"})
        except Exception as e:
            print(e.message)
            return JsonResponse({'status': "0"})
    else:
        print("form invalid")
        return JsonResponse({'status': "0"})


@login_required(login_url='/userprofile/login/')
def list_images(request):
    # images = Image.objects.filter(user=request.user)
    images = Image.objects.filter()
    return render(request, 'gallery/list_images.html', {"images": images})


@login_required(login_url='/userprofile/login/')
@require_POST
@csrf_exempt
def del_image(request):
    print(request.POST)
    image_created = request.POST['image_id']

    # test = models.DateTimeField(image_created)
    print(image_created)
    try:
        image = Image.objects.get(id=image_created)
        print("image", image)
        image.delete()
        return JsonResponse({'status': "1"})
    except Exception as e:
        print(e)
        return JsonResponse({'status': "2"})
