from django.shortcuts import render
from .models import Product_List
from django.db.models import Min, Max

def add_product(request):
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        size = request.POST.get('size')
        
        if name and price and size:
            Product_List.objects.create(product_name=name, product_price=price, product_size=size)
    
    return render(request,'add_product.html')

def list_product(request):
    products = Product_List.objects.all()
    product_filter = request.GET.get('filter_by')
    products_value_filter = request.GET.get('filter_by_value')
    segments = request.GET.get('segments')

    if product_filter and products_value_filter and product_filter not in ["range", "range_size"]:
        filter_products = {f"{product_filter}__icontains": products_value_filter}
        products = products.filter(**filter_products)

    range_data = []
    if product_filter == "range" and products_value_filter:
            min_price, max_price = map(int, products_value_filter.split('-'))
            products = products.filter(product_price__gte=min_price, product_price__lte=max_price)

            if segments:
                segments = int(segments)
                if segments > 0:
                    step = (max_price - min_price) / segments
                    for i in range(segments):
                        start = min_price + i * step
                        end = min_price + (i + 1) * step
                        count = products.filter(product_price__gte=start, product_price__lt=end).count()
                        range_data.append({"range": f"{int(start)} - {int(end)}","count": count})
    
    if product_filter == "range_size" and products_value_filter:
            min_size, max_size = map(float, products_value_filter.split('-'))
            products = products.filter(product_size__gte=min_size, product_size__lte=max_size)

            if segments:
                segments = int(segments)
                if segments > 0:
                    step = (max_size - min_size) / segments
                    for i in range(segments):
                        start = min_size + i * step
                        end = min_size + (i + 1) * step
                        count = products.filter(product_size__gte=start, product_size__lt=end).count()
                        range_data.append({"range": f"{int(start)} - {int(end)}", "count": count})
                
    return render(request, 'product_list.html', {"products": products, "range_data": range_data})