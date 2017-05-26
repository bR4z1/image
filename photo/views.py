import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q

from wsgiref.util import FileWrapper
import mimetypes

from photo.forms import AlbumForm, UserForm, AlbumForm1
from .models import AlbumPhoto
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext

from PIL import Image, ImageFilter, ImageDraw 
import os
from artphoto.settings import BASE_DIR

IMAGE_FILE_TYPES = ['jpg', 'png']

def convertImage(request, album_id):
	if request.method == "POST":
		photo = AlbumPhoto.objects.get(pk = album_id)
		img = Image.open(photo.photo_logo.path)
		draw = ImageDraw.Draw(img) 
		width = img.size[0]
		height = img.size[1] 	
		pix = img.load() 

		if request.POST['preset'] == 'L':
			img = img.convert("L") 

		if request.POST['preset'] == 'BLUR':
			img == img.filter(ImageFilter.BLUR)

		if request.POST['preset'] == 'FIND_EDGES':
			img = img.filter(ImageFilter.FIND_EDGES)

		if request.POST['preset'] == "1":
			img = img.convert("1")

		if request.POST['preset'] == "90":
			img = img.rotate(90)

		if request.POST['preset'] == "180":
			img = img.rotate(180)

		if request.POST['preset'] == "270":
			img = img.rotate(270)

		if request.POST['preset'] == "360":
			img = img.rotate(360)

		if request.POST['preset'] == "ghost":
			for i in range(width):
				for j in range(height):
					a = pix[i, j][0]
					b = pix[i, j][1]
					c = pix[i, j][2]
					draw.point((i, j), (255 - a, 255 - b, 255 - c))
		
		if request.POST['preset'] == "pixel":
			factor = 70
			for i in range(width):
				for j in range(height):
					rand = random.randint(-factor, factor)
					a = pix[i, j][0] + rand
					b = pix[i, j][1] + rand
					c = pix[i, j][2] + rand
					if (a < 0):
						a = 0
					if (b < 0):
						b = 0
					if (c < 0):
						c = 0
					if (a > 255):
						a = 255
					if (b > 255):
						b = 255
					if (c > 255):
						c = 255
					draw.point((i, j), (a, b, c)) 

		if request.POST['preset'] == "light":
			factor = 100
			for i in range(width):
				for j in range(height):
					a = pix[i, j][0] + factor
					b = pix[i, j][1] + factor
					c = pix[i, j][2] + factor
					if (a < 0):
						a = 0
					if (b < 0):
						b = 0
					if (c < 0):
						c = 0
					if (a > 255):
						a = 255
					if (b > 255):
						b = 255
					if (c > 255):
						c = 255
					draw.point((i, j), (a, b, c))

		if request.POST['preset'] == "night":
			factor = -100
			for i in range(width):
				for j in range(height):
					a = pix[i, j][0] + factor
					b = pix[i, j][1] + factor
					c = pix[i, j][2] + factor
					if (a < 0):
						a = 0
					if (b < 0):
						b = 0
					if (c < 0):
						c = 0
					if (a > 255):
						a = 255
					if (b > 255):
						b = 255
					if (c > 255):
						c = 255
					draw.point((i, j), (a, b, c))

		if request.POST['preset'] == "300":
			basewidth = 300
			wpercent = (basewidth / float(img.size[0]))
			hsize = int((float(img.size[1]) * float(wpercent)))
			img = img.resize((basewidth, hsize))
			
		if request.POST['preset'] == "128":
			basewidth = 128
			wpercent = (basewidth / float(img.size[0]))
			hsize = int((float(img.size[1]) * float(wpercent)))
			img = img.resize((basewidth, hsize))

		if request.POST['preset'] == "512":
			basewidth = 512
			wpercent = (basewidth / float(img.size[0]))
			hsize = int((float(img.size[1]) * float(wpercent)))
			img = img.resize((basewidth, hsize))

		if request.POST['preset'] == "return":
			photo = AlbumPhoto.objects.get(pk = album_id)
			photo_name = photo.photo_logo.name
			photo_way = os.path.join(BASE_DIR, 'media')
			name_resolution_img = photo_name.split('.')[1]
			if name_resolution_img == 'jpg':
				omg_img = photo_way +'/' + photo_name.split('.')[0] + '_' + str(album_id)+'.jpg'
			else:
				omg_img = photo_way +'/' + photo_name.split('.')[0] + '_' + str(album_id)+'.png'      
			img = Image.open(omg_img)
			img.save(photo_way + '/' + photo_name)
			img.close()
			return HttpResponseRedirect('http://localhost:8000/'+'photo/'+str(album_id)+'/detail_change/')

		if request.POST['preset'] == "return_main":
			photo = AlbumPhoto.objects.get(pk = album_id)
			photo_name = photo.photo_logo.name
			photo_way = os.path.join(BASE_DIR, 'media')
			name_resolution_img = photo_name.split('.')[1]
			if name_resolution_img == 'jpg':
				omg_img = photo_way +'/' + photo_name.split('.')[0] + '_' + str(album_id)+'.jpg'
			else:
				omg_img = photo_way +'/' + photo_name.split('.')[0] + '_' + str(album_id)+'.png'      
			img = Image.open(omg_img)
			img.save(photo_way + '/' + photo_name)
			img.close()
			return HttpResponseRedirect('http://localhost:8000/')
		img.save(photo.photo_logo.path)
		img.close()
		del draw
	return HttpResponseRedirect('http://localhost:8000/'+'photo/'+str(album_id)+'/detail_change/')



def get_image(request, album_id):
    photo = AlbumPhoto.objects.get(pk=album_id)
    photo_name = photo.photo_logo.name
    file_path = os.path.join(BASE_DIR, 'media') +"/"+ photo_name

    wrapper = FileWrapper(open(file_path, 'rb'))
    
    response = HttpResponse(wrapper, content_type="image/jpg")
    response['Content-Length'] = os.path.getsize(file_path)
    filename = "Image_%s.jpg" %(str(album_id))
    content = "attachment; filename='%s'" %(filename)
    response['Content-Disposition'] = content
    return response

class AlbumDelete(DeleteView):
	model = AlbumPhoto
	success_url = reverse_lazy('photo:index')  


def index(request):
	if not request.user.is_authenticated():
		return render(request, 'photo/index_no_user.html')
	else:
		photo_list = AlbumPhoto.objects.filter(user=request.user)
		query = request.GET.get("q")
		if query:
			photo_list = photo_list.filter(
				Q(photo_title__icontains=query)
			).distinct()
			return render(request, 'photo/index.html',{
				'photo_list': photo_list,
		
			})
		else:
			return render(request, 'photo/index.html', {"photo_list": photo_list})


def detail_change(request, album_id):
	albumphoto = get_object_or_404(AlbumPhoto, pk=album_id)
	return render(request,'photo/detail_change.html',{"albumphoto": albumphoto},)

def detail(request, album_id):
	if not request.user.is_authenticated():
		return render(request, 'photo/detail.html',{"albumphoto": albumphoto})
	else:
		form = AlbumForm1()
		photo = AlbumPhoto.objects.get(pk = album_id)
		name_o = photo.photo_logo.path.split('//')[-1]
		name_i = name_o.split('.')[0]
		name_r = name_o.split('.')[-1]
		photo_way = os.path.join(BASE_DIR, 'media')
		img = Image.open(photo.photo_logo.path)
		if name_r == 'jpg':
			img.save(name_i + '_' + str(album_id) + '.jpg')
		else:
			img.save(name_i + '_' + str(album_id) + '.png')
			
		img.close()
		user = request.user
		albumphoto = get_object_or_404(AlbumPhoto, pk=album_id)
		return render(request,'photo/detail.html',{"albumphoto": albumphoto, 'user': user, 'form': form})

def albumCreate(request):
	if not request.user.is_authenticated(): 
		return render(request, 'photo/check_login.html')
	else:
		form = AlbumForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			albumphoto = form.save(commit=False)
			albumphoto.user = request.user
			albumphoto.photo_logo = request.FILES['photo_logo']
			file_type = albumphoto.photo_logo.url.split('.')[-1]
			file_type = file_type.lower()
			if file_type not in IMAGE_FILE_TYPES:       
				context = {
					'photo': albumphoto,
					'form': form,
					'error_message': 'Image file must be JPG or PNG',
				}
				return render(request, 'photo/albumphoto_form.html', context)            
			albumphoto.save()
			return render(request, 'photo/detail_create.html', {'albumphoto': albumphoto})
		context = {
			"form": form,
		}
		return render(request, 'photo/albumphoto_form.html', context)

class UserFormView(View):
	form_class = UserForm
	template_name = 'photo/register.html'

	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			username = form.cleaned_data['username']
			password= form.cleaned_data['password']
			user.set_password(password)
			user.save()
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('photo:index')
		return render(request, self.template_name, {'form': form})

def logout_user(request):
	logout(request)
	form = UserForm(request.POST or None)
	context = {
		"form": form,
	}
	return render(request, 'photo/login.html', context)

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				photo_list = AlbumPhoto.objects.filter(user=request.user)
				return render(request, 'photo/index.html', {'photo_list': photo_list})
			else:
				return render(request, 'photo/login.html', {'error_message': 'Your account has been disabled'})
		else:
			return render(request, 'photo/login.html', {'error_message': 'Invalid login'})
	return render(request, 'photo/login.html')


