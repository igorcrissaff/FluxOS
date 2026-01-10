from .models import Product

def get_product(product_id):
    return Product.objects.get(id=product_id)

def list_products():
    return Product.objects.all()

def create_product(product_data):
    product = Product(**product_data)
    product.save()
    return product

def update_product(product_id, product_data):
    product = Product.objects.get(id=product_id)
    for attr, value in product_data.items():
        setattr(product, attr, value)
    product.save()
    return product

def delete_product(product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return {"message": "Product deleted successfully."}
