from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import HiddenInput, ModelForm

from teamspirit.preorders.models import ShoppingCartLine


class AddToCartForm(ModelForm):

    class Meta:
        model = ShoppingCartLine
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AddToCartForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-add-to-cart-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-4'
        self.helper.form_method = 'post'
        self.fields['shopping_cart'].widget = HiddenInput()
        self.fields['product'].widget = HiddenInput()
        self.helper.add_input(
            Submit('submit', 'Ajouter au panier', css_class="col-12")
        )
        if self.is_valid():
            self.save()


class DropFromCartForm(ModelForm):

    class Meta:
        model = ShoppingCartLine
        fields = []

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user')
        shopping_cart_line = kwargs.pop('shopping_cart_line')
        self.line_user = shopping_cart_line.shopping_cart.user
        self.shopping_cart_line = ShoppingCartLine.objects.get(
            id=kwargs.pop('line_id')
        )
        super(DropFromCartForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-drop-from-cart-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-4'
        self.helper.form_method = 'post'
        self.helper.add_input(
            Submit('submit', 'Confirmer', css_class="col-12")
        )
        if self.is_valid():
            self.save()

    def save(self, commit=True):
        if commit:
            # /!\ prevent this action for other users!
            if self.request_user == self.line_user:
                self.shopping_cart_line.delete()
        return self
