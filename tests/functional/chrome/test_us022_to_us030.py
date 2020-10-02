"""Contain the functional tests for the general User Stories.

The emulated web browser is Chrome.
Here are the User Stories, in French:
US022 - En tant que Toto, je veux accéder à la page de connexion pour me
        connecter à l'application.
US023 - En tant que Toto, je veux me connecter à l’application.
US024 - En tant que Toto, je veux accéder à la page d'accueil pour naviguer sur
        le site.
US025 - En tant que Toto, je veux accéder à chaque page de l'application pour
        naviguer sur le site.
US026 - En tant que Toto, je veux accéder à la page de contact pour communiquer
        avec le bureau de l'association.
US027 - En tant que Toto, je veux accéder à la page des mentions légales pour
        le plaisir.
US028 - En tant que Toto, je veux modifier mon mot de passe.
US029 - En tant que Toto, je veux réinitialiser mon mot de passe.
US030 - En tant que Toto, je veux me déconnecter de l’application.
"""

import re

from django.contrib.sites.models import Site
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import mail
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumlogin import force_login
from webdriver_manager.chrome import ChromeDriverManager

import config.settings.test as settings
from teamspirit.core.models import Address
from teamspirit.profiles.models import Personal
from teamspirit.users.models import User


class GeneralUserStoriesAnonymousTestCase(StaticLiveServerTestCase):
    """Contain the functional tests with anonymous user."""

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
        # two users in database
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
        self.user_a = User.objects.create_user(
            email="toto@mail.com",
            first_name="Toto",
            password="TopSecret",
            personal=self.personal
        )
        self.user_b = User.objects.create_user(
            email="titi@mail.com",
            first_name="Titi",
            password="Grosminet",
            is_active=False,
            personal=self.personal
        )

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def start_reset_password_process_step_1(self):
        """Method called in all US029-AT0x."""
        # start from the login page
        start_url = self.home_url + "users/login/"
        self.driver.get(start_url)
        # click on the link "Mot de passe oublié ?"
        reset_link = self.driver.find_element_by_id("forgotten_password")
        reset_link.click()
        # wait for page loading
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.url_changes(start_url))
        # redirect to the password reset page: True or False?
        expected_url = self.home_url + "profile/reset_password/"
        self.assertEqual(self.driver.current_url, expected_url)
        # change the site in the email
        site = Site.objects.get(id=settings.SITE_ID)
        site.domain = self.live_server_url
        site.name = self.live_server_url
        site.save()

    def start_reset_password_process_step_2(self):
        """Method called in US029-AT01 and US029-AT03."""
        # fill in the form with no error
        email_field = self.driver.find_element_by_id("id_email")
        email_field.send_keys("toto@mail.com")
        submit_button = self.driver.find_element_by_id("submit-id-submit")
        submit_button.click()
        # wait for email receiving
        actions = ActionChains(self.driver)
        actions.pause(1)
        actions.perform()
        # test that one message has been sent
        self.assertEqual(len(mail.outbox), 1)
        # get the mail content
        mail_content = mail.outbox[0].body
        # extract "reset password link"
        match = re.search(
            "choisir un nouveau mot de passe :\n(.*)\nPour mémoire",
            mail_content
        )
        return match

    def test_access_login_page(self):
        """US022-AT01: successful access to login page."""
        # ask for the login page
        start_url = self.home_url + "users/login/"
        self.driver.get(start_url)
        # check wether the page is reachable
        self.assertEqual(self.driver.current_url, start_url)

    def test_login_success(self):
        """US023-AT01: successful login."""
        # start from the login page
        start_url = self.home_url + "users/login/"
        self.driver.get(start_url)
        # fill the login form
        email_field = self.driver.find_element_by_id("id_username")
        email_field.send_keys("toto@mail.com")
        password_field = self.driver.find_element_by_id("id_password")
        password_field.send_keys("TopSecret")
        # click on the button "Se connecter"
        submit_button = self.driver.find_element_by_id("submit-id-submit")
        submit_button.click()
        # wait for page loading
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.url_changes(start_url))
        # redirect to home page: True or False?
        self.assertEqual(self.driver.current_url, self.home_url)
        # user authenticated: True or False?
        custom_welcome = self.driver.find_element_by_id("custom_welcome")
        self.assertEqual(custom_welcome.text, "BIENVENUE TOTO")

    def test_login_failure_wrong_email(self):
        """US023-AT02: login failed with wrong email."""
        # start from the login page
        start_url = self.home_url + "users/login/"
        self.driver.get(start_url)
        # fill the login form
        email_field = self.driver.find_element_by_id("id_username")
        email_field.send_keys("fail@mail.com")
        password_field = self.driver.find_element_by_id("id_password")
        password_field.send_keys("TopSecret")
        # click on the button "Se connecter"
        submit_button = self.driver.find_element_by_id("submit-id-submit")
        submit_button.click()
        # get an error message: True or False?
        error_message = self.driver.find_element_by_xpath(
            "//div[@class='alert alert-block alert-danger']/ul/li"
        )
        message_1 = "Please enter a correct Email and password. Note that " \
            "both fields may be case-sensitive."
        message_2 = "Saisissez un Courriel et un mot de passe valides. " \
            "Remarquez que chacun de ces champs est sensible à la casse " \
            "(différenciation des majuscules/minuscules)."
        self.assertTrue(
            (error_message.text == message_1) or
            (error_message.text == message_2)
        )
        # stay on current page: True or False?
        self.assertEqual(self.driver.current_url, start_url)

    def test_login_failure_wrong_password(self):
        """US023-AT03: login failed with wrong password."""
        # start from the login page
        start_url = self.home_url + "users/login/"
        self.driver.get(start_url)
        # fill the login form
        email_field = self.driver.find_element_by_id("id_username")
        email_field.send_keys("toto@mail.com")
        password_field = self.driver.find_element_by_id("id_password")
        password_field.send_keys("WrongPassword")
        # click on the button "Se connecter"
        submit_button = self.driver.find_element_by_id("submit-id-submit")
        submit_button.click()
        # get an error message: True or False?
        error_message = self.driver.find_element_by_xpath(
            "//div[@class='alert alert-block alert-danger']/ul/li"
        )
        message_1 = "Please enter a correct Email and password. Note that " \
            "both fields may be case-sensitive."
        message_2 = "Saisissez un Courriel et un mot de passe valides. " \
            "Remarquez que chacun de ces champs est sensible à la casse " \
            "(différenciation des majuscules/minuscules)."
        self.assertTrue(
            (error_message.text == message_1) or
            (error_message.text == message_2)
        )
        # stay on current page: True or False?
        self.assertEqual(self.driver.current_url, start_url)

    def test_login_failure_inactive_user(self):
        """US023-AT04: login failed with inactive user."""
        # start from the login page
        start_url = self.home_url + "users/login/"
        self.driver.get(start_url)
        # fill the login form
        email_field = self.driver.find_element_by_id("id_username")
        email_field.send_keys("titi@mail.com")
        password_field = self.driver.find_element_by_id("id_password")
        password_field.send_keys("Grosminet")
        # click on the button "Se connecter"
        submit_button = self.driver.find_element_by_id("submit-id-submit")
        submit_button.click()
        # get an error message: True or False?
        error_message = self.driver.find_element_by_xpath(
            "//div[@class='alert alert-block alert-danger']/ul/li"
        )
        message_1 = "Please enter a correct Email and password. Note that " \
            "both fields may be case-sensitive."
        message_2 = "Saisissez un Courriel et un mot de passe valides. " \
            "Remarquez que chacun de ces champs est sensible à la casse " \
            "(différenciation des majuscules/minuscules)."
        self.assertTrue(
            (error_message.text == message_1) or
            (error_message.text == message_2)
        )
        # stay on current page: True or False?
        self.assertEqual(self.driver.current_url, start_url)

    def test_reset_password_success(self):
        """US029-AT01: successful reset of password."""
        # start the process - step #1
        self.start_reset_password_process_step_1()
        # start the process - step #2
        match = self.start_reset_password_process_step_2()
        if not match:
            self.assertTrue("The email format is good!")
        else:
            reset_pwd_link = match.group(1)
            # enter the given link to the web browser
            self.driver.get(reset_pwd_link)
            edit_new_pwd_url = self.driver.current_url
            # fill in the form with no error (provide new password)
            new_pwd_field1 = self.driver.find_element_by_id(
                "id_new_password1"
            )
            new_pwd_field1.send_keys("TopSecret123")
            new_pwd_field2 = self.driver.find_element_by_id(
                "id_new_password2"
            )
            new_pwd_field2.send_keys("TopSecret123")
            submit_button = self.driver.find_element_by_id("submit-id-submit")
            submit_button.click()
            # wait for page loading
            WebDriverWait(
                self.driver,
                timeout=10
            ).until(EC.url_changes(edit_new_pwd_url))
            # check final url
            ok_url = f"{self.live_server_url}/profile/reset_password_complete/"
            self.assertEqual(self.driver.current_url, ok_url)

    def test_reset_password_failure_wrong_email(self):
        """US029-AT02: reset of password fails, wrong email."""
        # start the process - step #1
        self.start_reset_password_process_step_1()
        # fill in the form with an error (wrong email)
        email_field = self.driver.find_element_by_id("id_email")
        email_field.send_keys("error@mail.com")
        submit_button = self.driver.find_element_by_id("submit-id-submit")
        submit_button.click()
        # wait for email receiving
        actions = ActionChains(self.driver)
        actions.pause(1)
        actions.perform()
        # test that no message has been sent
        self.assertEqual(len(mail.outbox), 0)

    def test_reset_password_failure_different_new_passwords(self):
        """US029-AT03: reset of password fails, different new passwords."""
        # start the process - step #1
        self.start_reset_password_process_step_1()
        # start the process - step #2
        match = self.start_reset_password_process_step_2()
        if not match:
            self.assertTrue("The email format is good!")
        else:
            reset_pwd_link = match.group(1)
            # enter the given link to the web browser
            self.driver.get(reset_pwd_link)
            edit_new_pwd_url = self.driver.current_url
            # fill in the form with an error: different two passwords
            new_pwd_field1 = self.driver.find_element_by_id(
                "id_new_password1"
            )
            new_pwd_field1.send_keys("TopSecret123")
            new_pwd_field2 = self.driver.find_element_by_id(
                "id_new_password2"
            )
            new_pwd_field2.send_keys("TopSecret456")
            submit_button = self.driver.find_element_by_id("submit-id-submit")
            submit_button.click()
            # get an error message: True or False?
            error_message = self.driver.find_element_by_id(
                "error_1_id_new_password2"
            )
            message_1 = "The two password fields didn’t match."
            message_2 = "Les deux mots de passe ne correspondent pas."
            self.assertTrue(
                (error_message.text == message_1) or
                (error_message.text == message_2)
            )
            # stay on current page: True or False?
            self.assertEqual(self.driver.current_url, edit_new_pwd_url)


class GeneralUserStoriesAuthenticatedTestCase(StaticLiveServerTestCase):
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
            password="TopSecret",
            personal=self.personal
        )
        # force login for this user
        force_login(self.user, self.driver, self.live_server_url)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def start_change_password_process_step_1(self):
        """Method called in US028-AT0x."""
        # start from the home page
        start_url = self.home_url
        self.driver.get(start_url)
        # click on the link "Mon espace"
        toggler = self.driver.find_elements_by_class_name(
            'navbar-toggler-icon'
        )[0]
        toggler.click()
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.element_to_be_clickable((
            By.ID,
            "private_space_link"
        ))).click()
        # wait for page loading
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.url_changes(start_url))
        # check the new url
        expected_url_1 = start_url + "profile/"
        return expected_url_1

    def start_change_password_process_step_2(self, expected_url_1):
        """Method called in US028-AT0x."""
        # click on the button "Changer de mot de passe"
        change_password_button = self.driver.find_element_by_id(
            "change_password_button"
        )
        change_password_button.click()
        # wait for page loading
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.url_changes(expected_url_1))
        # check the new url
        expected_url_2 = expected_url_1 + "change_password/?"
        return expected_url_2

    def test_access_home_page(self):
        """US024-AT01: successful access to home page."""
        # request the home page
        start_url = self.home_url
        self.driver.get(start_url)
        # check wether the page is reachable
        self.assertEqual(self.driver.current_url, start_url)

    def test_access_events_page(self):
        """US025-AT01: successful access to events page."""
        # request the events page
        start_url = self.home_url + "events/"
        self.driver.get(start_url)
        # check wether the page is reachable
        self.assertEqual(self.driver.current_url, start_url)

    def test_access_trainings_page(self):
        """US025-AT02: successful access to trainings page."""
        # request the trainings page
        start_url = self.home_url + "trainings/"
        self.driver.get(start_url)
        # check wether the page is reachable
        self.assertEqual(self.driver.current_url, start_url)

    def test_access_catalog_page(self):
        """US025-AT03: successful access to catalog page."""
        # request the catalog page
        start_url = self.home_url + "catalog/"
        self.driver.get(start_url)
        # check wether the page is reachable
        self.assertEqual(self.driver.current_url, start_url)

    def test_access_private_space_page(self):
        """US025-AT04: successful access to private space page."""
        # request the private space page
        start_url = self.home_url + "profile/"
        self.driver.get(start_url)
        # check wether the page is reachable
        self.assertEqual(self.driver.current_url, start_url)

    def test_access_contact_page(self):
        """US026-AT01: successful access to contact page."""
        # request the contact page
        start_url = self.home_url + "contact/"
        self.driver.get(start_url)
        # check wether the page is reachable
        self.assertEqual(self.driver.current_url, start_url)

    def test_access_legal_page(self):
        """US027-AT01: successful access to legal page."""
        # request the contact page
        start_url = self.home_url + "legal/"
        self.driver.get(start_url)
        # check wether the page is reachable
        self.assertEqual(self.driver.current_url, start_url)

    def test_change_password_success(self):
        """US028-AT01: successful change of password."""
        # start the process - step #1
        expected_url_1 = self.start_change_password_process_step_1()
        self.assertEqual(self.driver.current_url, expected_url_1)
        # start the process - step #2
        expected_url_2 = self.start_change_password_process_step_2(
            expected_url_1
        )
        self.assertEqual(self.driver.current_url, expected_url_2)
        # fill the change password form
        old_password_field = self.driver.find_element_by_id("id_old_password")
        old_password_field.send_keys("TopSecret")
        new_password1_field = self.driver.find_element_by_id(
            "id_new_password1"
        )
        new_password1_field.send_keys("FooBarFooBar123")
        new_password2_field = self.driver.find_element_by_id(
            "id_new_password2"
        )
        new_password2_field.send_keys("FooBarFooBar123")
        # click on the button "Modifier le mot de passe"
        submit_button = self.driver.find_element_by_id("submit-id-submit")
        submit_button.click()
        # # wait for page loading
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.url_changes(expected_url_2))
        # check the final url
        expected_url_3 = expected_url_1 + "change_password/done/"
        self.assertEqual(self.driver.current_url, expected_url_3)

    def test_change_password_failure_wrong_old_password(self):
        """US028-AT02: change of password fails, wrong old password."""
        # start the process - step #1
        expected_url_1 = self.start_change_password_process_step_1()
        self.assertEqual(self.driver.current_url, expected_url_1)
        # start the process - step #2
        expected_url_2 = self.start_change_password_process_step_2(
            expected_url_1
        )
        self.assertEqual(self.driver.current_url, expected_url_2)
        # fill the change password form
        old_password_field = self.driver.find_element_by_id("id_old_password")
        old_password_field.send_keys("FailingPassword")
        new_password1_field = self.driver.find_element_by_id(
            "id_new_password1"
        )
        new_password1_field.send_keys("FooBarFooBar123")
        new_password2_field = self.driver.find_element_by_id(
            "id_new_password2"
        )
        new_password2_field.send_keys("FooBarFooBar123")
        # click on the button "Modifier le mot de passe"
        submit_button = self.driver.find_element_by_id("submit-id-submit")
        submit_button.click()
        # get an error message: True or False?
        error_message = self.driver.find_element_by_id(
            "error_1_id_old_password"
        )
        message_1 = "Your old password was entered incorrectly. " \
            "Please enter it again."
        message_2 = "Votre ancien mot de passe est incorrect. " \
            "Veuillez le rectifier."
        self.assertTrue(
            (error_message.text == message_1) or
            (error_message.text == message_2)
        )
        # stay on current page: True or False?
        self.assertEqual(self.driver.current_url, expected_url_2)

    def test_change_password_failure_different_new_passwords(self):
        """US028-AT03: change of password fails, different new passwords."""
        # start the process - step #1
        expected_url_1 = self.start_change_password_process_step_1()
        self.assertEqual(self.driver.current_url, expected_url_1)
        # start the process - step #2
        expected_url_2 = self.start_change_password_process_step_2(
            expected_url_1
        )
        self.assertEqual(self.driver.current_url, expected_url_2)
        # fill the change password form
        old_password_field = self.driver.find_element_by_id("id_old_password")
        old_password_field.send_keys("TopSecret")
        new_password1_field = self.driver.find_element_by_id(
            "id_new_password1"
        )
        new_password1_field.send_keys("FooBarFooBar123")
        new_password2_field = self.driver.find_element_by_id(
            "id_new_password2"
        )
        new_password2_field.send_keys("FooBarFooBar456")
        # click on the button "Modifier le mot de passe"
        submit_button = self.driver.find_element_by_id("submit-id-submit")
        submit_button.click()
        # get an error message: True or False?
        error_message = self.driver.find_element_by_id(
            "error_1_id_new_password2"
        )
        message_1 = "The two password fields didn’t match."
        message_2 = "Les deux mots de passe ne correspondent pas."
        self.assertTrue(
            (error_message.text == message_1) or
            (error_message.text == message_2)
        )
        # stay on current page: True or False?
        self.assertEqual(self.driver.current_url, expected_url_2)

    def test_logout(self):
        """US030-AT01: successful logout."""
        # start from the home page
        start_url = self.home_url
        self.driver.get(start_url)
        # click on the link "Déconnexion"
        toggler = self.driver.find_elements_by_class_name(
            'navbar-toggler-icon'
        )[0]
        toggler.click()
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.element_to_be_clickable((By.ID, "logout_link"))).click()
        # wait for page loading
        WebDriverWait(
            self.driver,
            timeout=10
        ).until(EC.url_changes(start_url))
        # redirect to logout page: True or False?
        logout_url = self.home_url + "users/logout/"
        self.assertEqual(self.driver.current_url, logout_url)
