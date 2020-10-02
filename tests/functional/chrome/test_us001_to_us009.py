"""Contain the functional tests for the User Stories played by members.

The emulated web browser is Chrome.
Here are the User Stories, in French:
US001 - En tant que Laurent, je veux indiquer mes coordonnées pour être
        joignable par d’autres adhérents.
US002 - En tant que Laurent, je veux poster un fichier sur la plateforme pour
        transmettre mon certificat médical.
US003 - En tant que Laurent, je veux renseigner des informations à destination
        des adhérents pour proposer des créneaux d'entraînement.
US004 - En tant que Claire, je veux consulter l'agenda pour connaître les
        événements passés et à venir.
US005 - En tant que Claire, je veux télécharger ou ouvrir un document pour lire
        un compte-rendu de réunion.
US006 - En tant que Pierre, je veux accéder à certaines informations des
        adhérents pour rencontrer d'autres coureurs.
US007 - En tant que Pierre, je veux consulter la liste des articles disponibles
        pour obtenir une tenue de sport.
US008 - En tant que Pierre, je veux renseigner une pré-commande pour obtenir
        une tenue de sport.
US009 - En tant que Pierre, je veux connaître les adhérents intéressés par une
        pratique en groupe pour s'entraîner ensemble.
"""

import os
import re

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.files.uploadedfile import UploadedFile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumlogin import force_login
from webdriver_manager.chrome import ChromeDriverManager

from teamspirit.catalogs.models import Catalog, Product
from teamspirit.core.models import Address
from teamspirit.preorders.models import ShoppingCart
from teamspirit.profiles.models import Personal
from teamspirit.users.models import User


class NoStaffUserStoriesAuthenticatedTestCase(StaticLiveServerTestCase):
    """Contain the functional tests with authenticated user."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # initialize a webdriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        cls.driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=chrome_options
        )
        # set home_url
        cls.home_url = f"{cls.live_server_url}/"

    def setUp(self):
        super().setUp()
        # a user in database
        self.address = Address.objects.create(
            label_first="1 rue de l'impasse",
            label_second="",
            postal_code="75000",
            city="Paris",
            country="France"
        )
        self.personal = Personal.objects.create(
            phone_number="01 02 03 04 05",
            address=self.address
        )
        self.user = User.objects.create_user(
            email="toto@mail.com",
            first_name="Toto",
            last_name="LE RIGOLO",
            password="TopSecret",
            personal=self.personal
        )
        # force login for this user
        force_login(self.user, self.driver, self.live_server_url)
        # some other data
        self.shopping_cart = ShoppingCart.objects.create(
            user=self.user,
        )
        self.catalog = Catalog.objects.create(
            name="Catalogue de vêtements",
        )
        self.file = os.getcwd() + "/tests/functional/files/survetement.jpg"
        self.image = UploadedFile(file=self.file)
        self.product_a = Product.objects.create(
            name="Produit A",
            image=self.image,
            is_available=True,
            is_free=False,
            price=25,
            catalog=self.catalog,
        )
        self.product_b = Product.objects.create(
            name="Produit B",
            image=self.image,
            is_available=True,
            is_free=False,
            price=100,
            catalog=self.catalog,
        )

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_update_last_name_and_first_name(self):
        """US001-AT01: successful update of last name and first name."""
        # ask for the profile page
        start_url = self.home_url + "profile/"
        self.driver.get(start_url)
        # click on the tab "Etat civil"
        names_tab = self.driver.find_element_by_id("etat-civil")
        names_tab.click()
        # click on the button "Modifier"
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.element_to_be_clickable((
            By.ID,
            "change_names_button"
        ))).click()
        # wait for page loading
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.url_changes(start_url))
        # check wether the page is reachable
        expected_url = start_url + "update_personal_info/?"
        self.assertEqual(self.driver.current_url, expected_url)
        # update data
        last_name_field = self.driver.find_element_by_id("id_last_name")
        last_name_field.clear()
        last_name_field.send_keys("le rikiki")
        first_name_field = self.driver.find_element_by_id("id_first_name")
        first_name_field.clear()
        first_name_field.send_keys("titi")
        # click on the button "Mettre à jour"
        submit_button = self.driver.find_element_by_id("submit-id-submit")
        submit_button.click()
        # wait for page loading
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.url_changes(expected_url))
        # check wether the page is reachable
        self.assertEqual(self.driver.current_url, start_url)
        # check wether data are updated
        names_tab = self.driver.find_element_by_id("etat-civil")
        names_tab.click()
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.element_to_be_clickable((
            By.ID,
            "change_names_button"
        )))
        last_name_field = self.driver.find_element_by_id("last_name_field")
        last_name_value = last_name_field.get_attribute("value")
        self.assertEqual(last_name_value, "LE RIKIKI")
        first_name_field = self.driver.find_element_by_id("first_name_field")
        first_name_value = first_name_field.get_attribute("value")
        self.assertEqual(first_name_value, "Titi")

    def test_update_phone_and_address(self):
        """US001-AT02: successful update of phone number and address."""
        # ask for the profile page
        start_url = self.home_url + "profile/"
        self.driver.get(start_url)
        # click on the tab "Coordonnées"
        contact_info_tab = self.driver.find_element_by_id("coordonnees")
        contact_info_tab.click()
        # click on the button "Modifier"
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.element_to_be_clickable((
            By.ID,
            "update_phone_address"
        ))).click()
        # wait for page loading
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.url_changes(start_url))
        # check wether the page is reachable
        expected_url = start_url + "update_phone_address/?"
        self.assertEqual(self.driver.current_url, expected_url)
        # update data
        phone_field = self.driver.find_element_by_id("id_phone_number")
        phone_field.clear()
        phone_field.send_keys("99 98 97 96 95")
        label_first_field = self.driver.find_element_by_id("id_label_first")
        label_first_field.clear()
        label_first_field.send_keys("12 rue du Pont")
        label_second_field = self.driver.find_element_by_id("id_label_second")
        label_second_field.clear()
        label_second_field.send_keys("Appartement 3")
        postal_code_field = self.driver.find_element_by_id("id_postal_code")
        postal_code_field.clear()
        postal_code_field.send_keys("79000")
        city_field = self.driver.find_element_by_id("id_city")
        city_field.clear()
        city_field.send_keys("Niort")
        country_field = self.driver.find_element_by_id("id_country")
        country_field.clear()
        country_field.send_keys("Suisse")
        confidentiality_checkbox_label = self.driver.find_element_by_xpath(
            "//label[@for='id_has_private_profile']"
        )
        confidentiality_checkbox_label.click()
        # click on the button "Mettre à jour"
        submit_button = self.driver.find_element_by_id(
            "submit-phone-address-form"
        )
        submit_button.click()
        # wait for page loading
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.url_changes(expected_url))
        # check wether the page is reachable
        self.assertEqual(self.driver.current_url, start_url)
        # check wether data are updated
        contact_info_tab = self.driver.find_element_by_id("coordonnees")
        contact_info_tab.click()
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.element_to_be_clickable((
            By.ID,
            "update_phone_address"
        )))
        phone_field = self.driver.find_element_by_id("phone_field")
        phone_value = phone_field.get_attribute("value")
        self.assertEqual(phone_value, "99 98 97 96 95")
        label_first_field = self.driver.find_element_by_id("label_first_field")
        first_name_value = label_first_field.get_attribute("value")
        self.assertEqual(first_name_value, "12 rue du Pont - Appartement 3")
        postal_code_and_city_field = self.driver.find_element_by_id(
            "postal_code_and_city_field"
        )
        postal_code_and_city_value = postal_code_and_city_field.get_attribute(
            "value"
        )
        self.assertEqual(postal_code_and_city_value, "79000 Niort")
        country_field = self.driver.find_element_by_id("country_field")
        country_value = country_field.get_attribute("value")
        self.assertEqual(country_value, "Suisse")
        confidentiality_checkbox = self.driver.find_element_by_id(
            "confidential_checkbox"
        )
        self.assertTrue(confidentiality_checkbox.is_selected())

    def test_add_then_drop_medical_file(self):
        """US002-AT01: add then drop a medical file."""
        # ask for the profile page
        start_url = self.home_url + "profile/"
        self.driver.get(start_url)
        # click on the tab "Certificat ou licence"
        medical_file_tab = self.driver.find_element_by_id("fichier-medical")
        medical_file_tab.click()
        # click on the button "Modifier"
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.element_to_be_clickable((
            By.ID,
            "add_medical_file_button"
        ))).click()
        # wait for page loading
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.url_changes(start_url))
        # check wether the page is reachable
        expected_url = start_url + "add_medical_file/?"
        self.assertEqual(self.driver.current_url, expected_url)
        # upload a file
        add_file_button = self.driver.find_element_by_id("id_medical_file")
        add_file_button.send_keys(
            os.getcwd() + "/tests/functional/files/toto_medical_file.png"
        )
        # submit the form
        submit_button = self.driver.find_element_by_id("submit-id-submit")
        submit_button.click()
        # wait for page loading
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.url_to_be(start_url))
        # click on the tab "Certificat ou licence"
        medical_file_tab = self.driver.find_element_by_id("fichier-medical")
        medical_file_tab.click()
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.element_to_be_clickable((
            By.ID,
            "drop_medical_file_button"
        )))
        # check wether the file name is present and correct
        medical_file_link = self.driver.find_element_by_id(
            "medical_file_name"
        )
        medical_file_name = medical_file_link.text
        expected_regex = r'lic/LE RIGOLO_Toto/toto_medical_file.*\.png'
        self.assertTrue(re.match(expected_regex, medical_file_name))
        # drop the file
        drop_file_button = self.driver.find_element_by_id(
            "drop_medical_file_button"
        )
        drop_file_button.click()
        # wait for page loading
        expected_url = start_url + "drop_medical_file/?"
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.url_to_be(expected_url))
        # click on the button "Confirmer"
        submit_button = self.driver.find_element_by_id("submit-id-submit")
        submit_button.click()
        # wait for page loading
        expected_url = start_url + "drop_file/"
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.url_to_be(expected_url))
        # click on the button "Retour"
        back_button = self.driver.find_element_by_id("back_button")
        back_button.click()
        # wait for page loading
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.url_changes(expected_url))
        # check wether we come back at profile page
        self.assertEqual(self.driver.current_url, start_url)
        # click on the tab "Certificat ou licence"
        medical_file_tab = self.driver.find_element_by_id("fichier-medical")
        medical_file_tab.click()
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.element_to_be_clickable((
            By.ID,
            "add_medical_file_button"
        )))
        # check wether the file name is empty
        medical_file_field = self.driver.find_element_by_id(
            "medical_file_name"
        )
        medical_file_name = medical_file_field.get_attribute("value")
        self.assertEqual(medical_file_name, 'Aucun fichier sélectionné')

    def test_add_then_drop_id_file(self):
        """US002-AT02: add then drop an id file."""
        # ask for the profile page
        start_url = self.home_url + "profile/"
        self.driver.get(start_url)
        # click on the tab "Certificat ou licence"
        id_file_tab = self.driver.find_element_by_id("fichier-identite")
        id_file_tab.click()
        # click on the button "Modifier"
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.element_to_be_clickable((
            By.ID,
            "add_id_file_button"
        ))).click()
        # wait for page loading
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.url_changes(start_url))
        # check wether the page is reachable
        expected_url = start_url + "add_id_file/?"
        self.assertEqual(self.driver.current_url, expected_url)
        # upload a file
        add_file_button = self.driver.find_element_by_id("id_id_file")
        add_file_button.send_keys(
            os.getcwd() + "/tests/functional/files/toto_id_file.png"
        )
        # submit the form
        submit_button = self.driver.find_element_by_id("submit-id-submit")
        submit_button.click()
        # wait for page loading
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.url_to_be(start_url))
        # click on the tab "Certificat ou licence"
        id_file_tab = self.driver.find_element_by_id("fichier-identite")
        id_file_tab.click()
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.element_to_be_clickable((
            By.ID,
            "drop_id_file_button"
        )))
        # check wether the file name is present and correct
        id_file_link = self.driver.find_element_by_id("id_file_name")
        id_file_name = id_file_link.text
        expected_regex = r'id/LE RIGOLO_Toto/toto_id_file.*\.png'
        self.assertTrue(re.match(expected_regex, id_file_name))
        # drop the file
        drop_file_button = self.driver.find_element_by_id(
            "drop_id_file_button"
        )
        drop_file_button.click()
        # wait for page loading
        expected_url = start_url + "drop_id_file/?"
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.url_to_be(expected_url))
        # click on the button "Confirmer"
        submit_button = self.driver.find_element_by_id("submit-id-submit")
        submit_button.click()
        # wait for page loading
        expected_url = start_url + "drop_file/"
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.url_to_be(expected_url))
        # click on the button "Retour"
        back_button = self.driver.find_element_by_id("back_button")
        back_button.click()
        # wait for page loading
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.url_changes(expected_url))
        # check wether we come back at profile page
        self.assertEqual(self.driver.current_url, start_url)
        # click on the tab "Certificat ou licence"
        id_file_tab = self.driver.find_element_by_id("fichier-identite")
        id_file_tab.click()
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.element_to_be_clickable((
            By.ID,
            "add_id_file_button"
        )))
        # check wether the file name is empty
        id_file_field = self.driver.find_element_by_id("id_file_name")
        id_file_name = id_file_field.get_attribute("value")
        self.assertEqual(id_file_name, 'Aucun fichier sélectionné')

    def test_consult_catalog_items(self):
        """US007-AT01: consult the catalog items."""
        # request the catalog page
        start_url = self.home_url + "catalog/"
        self.driver.get(start_url)
        # count the number of products
        products_list = self.driver.find_elements_by_link_text(
            "Ajouter au panier"
        )
        self.assertEqual(len(products_list), 2)

    def test_add_then_delete_a_product_from_shopping_cart(self):
        """US008-AT01: add then drop a product from shopping cart."""
        # request the catalog page
        start_url = self.home_url + "catalog/"
        self.driver.get(start_url)
        # click on the first button "Ajouter au panier"
        add_to_cart_button = self.driver.find_elements_by_link_text(
            "Ajouter au panier"
        )[0]
        add_to_cart_button.click()
        # wait for page loading
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.url_changes(start_url))
        # check wether the page is reachable
        expected_url_start = self.home_url + "shopping_cart/add_product/"
        self.assertTrue(self.driver.current_url.startswith(expected_url_start))
        # update data
        last_name_field = self.driver.find_element_by_id("id_size")
        last_name_field.send_keys("M")
        # click on the button "Ajouter au panier"
        submit_button = self.driver.find_element_by_id("submit-id-submit")
        submit_button.click()
        # wait for page loading
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.url_to_be(start_url))
        # click on the link "Voir mon panier"
        cart_link = self.driver.find_element_by_link_text("Voir mon panier")
        cart_link.click()
        # wait for page loading
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.url_changes(start_url))
        # check wether the page is reachable
        expected_url = self.home_url + "shopping_cart/"
        self.assertEqual(self.driver.current_url, expected_url)
        # click on the button "Supprimer"
        delete_button = self.driver.find_element_by_link_text("Supprimer")
        delete_button.click()
        # wait for page loading
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.url_changes(expected_url))
        # check wether the page is reachable
        new_url_start = self.home_url + "shopping_cart/drop_product/"
        self.assertTrue(self.driver.current_url.startswith(new_url_start))
        # click on the button "Confirmer"
        submit_button = self.driver.find_element_by_id("submit-id-submit")
        submit_button.click()
        # wait for page loading
        expected_url = self.home_url + "shopping_cart/"
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.url_to_be(expected_url))
        # check wether the cart is empty
        p_list = self.driver.find_elements_by_tag_name('p')
        self.assertEqual(p_list[0].text, "Montant total du panier : 0 €")
        self.assertEqual(
            p_list[1].text,
            "Votre panier de pré-commande est vide !"
        )
