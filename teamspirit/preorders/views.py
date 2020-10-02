from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormView

from teamspirit.catalogs.models import Product
from teamspirit.preorders.forms import AddToCartForm, DropFromCartForm
from teamspirit.preorders.models import ShoppingCart, ShoppingCartLine


class ShoppingCartView(ListView):

    model = ShoppingCartLine
    template_name = "preorders/shopping_cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shopping_cart_amount'] = ShoppingCart.objects.get_or_create(
            user=self.request.user
        )[0].get_cart_amount()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        shopping_cart = ShoppingCart.objects.get_or_create(
            user=self.request.user
        )[0]
        queryset = ShoppingCartLine.objects.filter(
            shopping_cart=shopping_cart
        )
        return queryset


shopping_cart_view = ShoppingCartView.as_view()
shopping_cart_view = login_required(shopping_cart_view)


class AddToCartView(FormView):

    template_name = "preorders/add_to_cart.html"
    form_class = AddToCartForm
    success_url = reverse_lazy('catalogs:catalog')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(id=self.kwargs['product_id'])
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['shopping_cart'] = ShoppingCart.objects.get_or_create(
            user=self.request.user
        )[0]
        initial['product'] = Product.objects.get(id=self.kwargs['product_id'])
        return initial


add_to_cart_view = AddToCartView.as_view()
add_to_cart_view = login_required(add_to_cart_view)


class DropFromCartView(FormView):

    template_name = "preorders/drop_from_cart.html"
    form_class = DropFromCartForm
    success_url = reverse_lazy('preorders:shopping_cart')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shopping_cart_line'] = ShoppingCartLine.objects.get(
            id=self.kwargs['line_id']
        )
        return context

    def get_form_kwargs(self):
        kwargs = super(DropFromCartView, self).get_form_kwargs()
        kwargs.update({'request_user': self.request.user})
        kwargs.update({'line_id': self.kwargs['line_id']})
        kwargs.update({
            'shopping_cart_line': ShoppingCartLine.objects.get(
                id=self.kwargs['line_id']
            )
        })
        return kwargs


drop_from_cart_view = DropFromCartView.as_view()
drop_from_cart_view = login_required(drop_from_cart_view)
