from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View

from .models import Category, Cart, Customer, Notebook, Smartphone

class CategoryDetailMixin(SingleObjectMixin):

    CATEGORY_MODEL2PRODUCT_MODEL = {
        'notebooks': Notebook,
        'smartphones': Smartphone
    }

    def get_context_data(self, **kwargs):
        if isinstance(self.get_object(), Category):
            model = self.CATEGORY_MODEL2PRODUCT_MODEL[self.get_object().slug]
            contex = super().get_context_data(**kwargs)
            contex['categories'] = Category.objects.get_categories_for_left_sidebar()
            contex['category_products'] = model.objects.all()
            return contex
        contex = super().get_context_data(**kwargs)
        contex['categories'] = Category.objects.get_categories_for_left_sidebar()
        return contex

class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(
                    user=request.user
                )
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
        else:
            cart = Cart.objects.filter(for_anonymous_user=True).first()
            if not cart:
                cart = Cart.objects.create(for_anonymous_user=True)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)
