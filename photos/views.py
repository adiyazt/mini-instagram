from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseNotAllowed
from photos.models import User, Photo, Comment
from .models import filters as FILTERS
import PIL.Image
import pilgram
import uuid

FILTER_IMAGES = [
        ['images/lofi.jpg', 'lofi'],
        ['images/valencia.jpg', 'valencia'],
        ['images/brooklyn.jpg', 'brooklyn'],
        ['images/willow.jpg', 'willow'],
        ['images/gingham.jpg', 'gingham']
    ]



def index(request):
    if request.session.get('is_authorized'):
        auth = True
    else:
        auth = False
    photos = Photo.objects.all()
    return render(request, 'index.html', context={'auth': auth, 'photos' : photos})


def register(request):
    template = 'register.html'
    if request.session.get('is_authorized'):
        return redirect('index')
    return render(request, template)


def login(request):
    template = 'login.html'
    if request.session.get('is_authorized'):
        return redirect('index')
    return render(request, template)


def deauth(request):
    if request.session.get('is_authorized'):
        request.session.clear()
    return redirect('index')


def api_auth(request):
    email   : str = request.POST.get('email')
    password: str = request.POST.get('password')

    print(f'{email=} {password=}')

    if email and password:
        if User.objects.filter(email=email, password=password).exists():
            user = User.objects.get(email=email, password=password)
            request.session['is_authorized'] = True
            request.session['email'] = user.email
            request.session['user_id'] = str(user.pk)
            print(f'{user.pk=}')
            return redirect('index')
        else:
            return HttpResponseBadRequest('User does not exist')
    return HttpResponseBadRequest('Invalid data')


def api_reg(request):
    name: str = request.POST.get('name')
    phone   : str = request.POST.get('phone')
    email   : str = request.POST.get('email')
    password: str = request.POST.get('password')
    cpassword   : str = request.POST.get('cpassword')

    if name and email and password and phone and cpassword:
        if User.objects.filter(email=email).exists():
            return HttpResponseBadRequest('User exists')
        if password != cpassword:
            return HttpResponseBadRequest('Passwords do not match')

        user: User = User()
        user.email = email
        user.full_name = name
        user.password = password
        user.phone = phone
        user.save()

        request.session['is_authorized'] = True
        request.session['email'] = user.email
        request.session['user_id'] = str(user.pk)

        return redirect('index')
    return HttpResponse('Invalid data', status=403)
        


def post_photo(request):
    if request.session['is_authorized']:
        if request.method == 'POST':
            print(request)
            print(request.FILES)
            text = request.POST.get('text')
            file = request.FILES['file']
            filter = request.POST.get('filter')
            user = request.session['user_id']
            download_photo(file, filter, text, user)
            return redirect('index')
        else:
            if request.session.get('is_authorized'):
                auth = True
            else:
                auth = False
            context = {
            'filters' : FILTERS,
            'filter_images' : FILTER_IMAGES,
            'auth' : auth
            }
            return render(request, 'post_photo.html', context)
        
        
def handle_upload_file(file):
    _filename = str(file)
    ext = _filename.split('.')[-1]
    if ext in ('jpg', 'png', 'jpeg'):
        id = str(uuid.uuid4())
        _path = f'photos/static/images/{id}.{ext}'

        with open(_path, 'wb+') as _file:
            for chunk in file.chunks():
                _file.write(chunk)
                
    return [id, ext]


def download_photo(file, filter, text, user):
    data = handle_upload_file(file)
    id, ext = data[0], data[1]
    if id:
        img = PIL.Image.open(f'photos/static/images/{id}.{ext}')
        extension = f'photos/static/users_images/{id}.{ext}'
        
        match filter:
            case 'brooklyn':
                pilgram.brooklyn(img).save(extension)
            case 'gingham':
                pilgram.gingham(img).save(extension)
            case 'lofi':
                pilgram.lofi(img).save(extension)
            case 'valencia':
                pilgram.valencia(img).save(extension)
            case 'willow':
                pilgram.willow(img).save(extension)
            case 'no':
                img.save(extension)
        
        
        photo: Photo = Photo()
        photo.id = id
        photo.source = f'/static/users_images/{id}.{ext}'
        photo.text = text
        photo.filter = filter
        photo.user = user
        photo.save()


def users(request):
    if request.session.get('is_authorized'):
        user_id=request.session['user_id']
        print(user_id)
        user = User.objects.get(pk=user_id)
        print(user)
        context = {
            'user' : user,
            'photos' : Photo.objects.filter(user=user.pk),
            'auth' : True
        }
        return render(request, 'users.html', context=context)
    return redirect('login')


def api_like(request, photo_id = None):
    try:
        if photo_id:
            photo = Photo.objects.get(id = photo_id)
            photo.likes = photo.likes + 1
            photo.save()
        return redirect('index')
    except Exception as e:
        print(Exception)
        
        
def api_dislike(request, photo_id = None):
    try:
        if photo_id:
            photo = Photo.objects.get(id = photo_id)
            photo.dislikes = photo.dislikes + 1
            photo.save()
        return redirect('index')
    except Exception as e:
        print(Exception)
        
        
def comments(request, photo_id = None):
    try:
        print(photo_id)
        if request.GET.get('text'):
            print(0000000000)
            print(request.GET.get('text'))
            comment = Comment()
            comment.photo = photo_id
            comment.user = request.session('user_id') if request.session('is_authorized') else 'Anonymous'
            print(comment.user)
            comment.text = request.GET.get('text')
            comment.save()
            print(comment)
        comments = Comment.objects.filter(photo=photo_id)
        context={'comments' : comments}
        return render(request, 'comments.html', context=context)
    except Exception as e:
        print(e)
        return HttpResponse('wrong')