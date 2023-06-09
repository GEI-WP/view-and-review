from behave import *
from selenium.webdriver.common.by import By

from web.models import User

use_step_matcher("parse")

@when('I register a new user')
def step_impl(context):
    for row in context.table:
        context.browser.get(context.get_url('register'))
        assert context.browser.current_url == context.get_url('register')
        context.browser.find_element(By.ID, 'id_email').send_keys(row['email'])
        context.browser.find_element(By.ID, 'id_username').send_keys(row['username'])
        context.browser.find_element(By.ID, 'id_password1').send_keys(row['password1'])
        context.browser.find_element(By.ID, 'id_password2').send_keys(row['password2'])
        context.browser.find_element(By.ID, 'register-button').click()
    assert User.objects.count() == 1
        
@then(u'I\'m viewing the main page')
def step_impl(context):
    assert context.get_url('index') in context.browser.current_url # Check if it is substring due to deep-linking
