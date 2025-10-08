import datetime
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm
from main.models import Product
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags

# --- Fungsi Main (Renderer) ---
@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")

    if filter_type == "all":
        products_list = Product.objects.all()
    else:
        products_list = Product.objects.filter(user=request.user)
        
    context = {
        'npm' : '2406409542',
        'name': 'Rafasya Muhammad Subhan',
        'class': 'PBP A',
        'products_list' : products_list,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }

    return render(request, "main.html", context)


# --- CREATE Product (Tradisional) ---
def add_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        products_entry = form.save(commit=False)
        products_entry.user = request.user
        products_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "add_product.html", context)

# --- CREATE Product (AJAX) ---
@login_required(login_url='/login')
@csrf_exempt
@require_POST
def add_product_ajax(request):
    form = ProductForm(request.POST)

    if form.is_valid():
        new_product = form.save(commit=False)
        new_product.user = request.user
        new_product.save()
        # Mengembalikan JSON dengan ID produk yang baru dibuat
        return JsonResponse({'status': 'success', 'id': new_product.pk, 'message': 'Produk berhasil ditambahkan!'}, status=201)
    else:
        # Mengambil pesan error pertama dari form
        errors = dict(form.errors)
        first_error_key = next(iter(errors))
        error_message = f"{first_error_key}: {errors[first_error_key][0]}"
        return JsonResponse({'status': 'error', 'message': error_message}, status=400)


# --- READ Product Detail (Tradisional) ---
@login_required(login_url='/login')
def show_product(request,id):
    products = get_object_or_404(Product, pk=id)
    # Asumsi fungsi add_visitor() ada di model Product
    # products.add_visitor() 

    context = {
        'product' : products
    }
    return render(request, "product_detail.html", context)

# --- DELETE Product (Tradisional) ---
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return redirect("main:show_main")

# --- DELETE Product (AJAX) ---
@login_required(login_url='/login')
@csrf_exempt
@require_POST
def delete_product_ajax(request, id):
    product = get_object_or_404(Product, pk=id)
    is_authorized = (request.user == product.user) or (request.user.username == "admin")
    
    if not is_authorized:
        return JsonResponse({'status': 'error', 'message': 'Akses ditolak: Anda tidak berhak menghapus produk ini.'}, status=403)
    
    product_name = product.name
    product.delete()
    # 204 No Content/Success (menggunakan 200 OK untuk memastikan body JsonResponse dikirim)
    return JsonResponse({'status': 'success', 'message': f"Produk '{product_name}' berhasil dihapus."}, status=200) 


# --- XML/JSON Feed (Tradisional) ---
def show_xml(request):
    products_list = Product.objects.all()
    xml_data = serializers.serialize("xml", products_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    products_list = Product.objects.all()
    json_data = serializers.serialize("json", products_list)
    return HttpResponse(json_data, content_type="application/json")

# By id
def show_xml_by_id(request, product_id):
    try:
        product_item = Product.objects.filter(pk=product_id)
        xml_data = serializers.serialize("xml", product_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except Product.DoesNotExist:
        return HttpResponse(status=404)

def show_json_by_id(request, product_id):
    try:
        product_item = Product.objects.get(pk=product_id)
        json_data = serializers.serialize("json", [product_item])
        return HttpResponse(json_data, content_type="application/json")
    except Product.DoesNotExist:
        return HttpResponse(status=404)
    
# --- AUTH (Tradisional) ---
def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

@login_required(login_url='/login')
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

# --- AUTH (AJAX) ---
@csrf_exempt
@require_POST
def login_ajax(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        redirect_url = reverse("main:show_main")
        resp = JsonResponse({'status': 'success', 'redirect_url': redirect_url, 'message': 'Login berhasil!'})
        resp.set_cookie('last_login', str(datetime.datetime.now()))
        return resp
        
    else:
        return JsonResponse({'status': 'error', 'message': 'Username atau password tidak valid.'}, status=400)
    
@csrf_exempt
@require_POST
def register_ajax(request):
    form = UserCreationForm(request.POST)
    
    if form.is_valid():
        form.save()
        login_url = reverse('main:login')
        return JsonResponse({'status': 'success', 'redirect_url': login_url, 'message': 'Akun berhasil dibuat! Silakan Login.'}, status=201)
    else:
        errors = dict(form.errors)
        # Ambil pesan error pertama
        first_error_key = next(iter(errors))
        error_message = f"{first_error_key}: {errors[first_error_key][0]}"
        return JsonResponse({'status': 'error', 'message': error_message}, status=400)
    
@login_required(login_url='/login')
@csrf_exempt
@require_POST
def logout_ajax(request):
    logout(request)
    redirect_url = reverse("main:login")
    resp = JsonResponse({'status': 'success', 'redirect_url': redirect_url, 'message': 'Logout berhasil!'})
    resp.delete_cookie('last_login')
    return resp


# --- EDIT/UPDATE Product (Tradisional) ---
@login_required(login_url='/login')
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')
    
    context = {
        'form' : form
    }

    return render(request, "edit_product.html", context)

# --- EDIT/UPDATE Product (AJAX) ---
@login_required(login_url='/login')
@csrf_exempt
@require_POST
def edit_product_ajax(request, id):
    product = get_object_or_404(Product, pk=id)
    is_authorized = (request.user == product.user) or (request.user.username == "admin")

    if not is_authorized:
        return JsonResponse({'status': 'error', 'message': 'Akses ditolak: Anda tidak berhak mengedit produk ini.'}, status=403)
    
    form = ProductForm(request.POST, instance=product)
    
    if form.is_valid():
        if 'is_featured' not in request.POST:
            form.instance.is_featured = False
        form.save()
        return JsonResponse({'status': 'success', 'message': 'Produk berhasil diperbarui!'}, status=200)
    else:
        errors = dict(form.errors)
        first_error_key = next(iter(errors))
        error_message = f"{first_error_key}: {errors[first_error_key][0]}"
        return JsonResponse({'status': 'error', 'message': error_message}, status=400)
    
@login_required(login_url='/login')
@csrf_exempt
@require_POST
def update_product_ajax(request, id):
    product = get_object_or_404(Product, pk=id)
    is_authorized = (request.user == product.user) or (request.user.username == "admin")
    
    if not is_authorized:
        return JsonResponse({'status': 'error', 'message': 'Akses ditolak: Anda tidak berhak mengedit produk ini.'}, status=403)

    form = ProductForm(request.POST, instance=product)
    
    if form.is_valid():
        if 'is_featured' not in request.POST:
            form.instance.is_featured = False
        
        form.save()
        return JsonResponse({'status': 'success', 'message': 'Produk berhasil diperbarui!'}, status=200)
    else:
        errors = dict(form.errors)
        first_error_key = next(iter(errors))
        error_message = f"{first_error_key}: {errors[first_error_key][0]}"
        return JsonResponse({'status': 'error', 'message': error_message}, status=400)
