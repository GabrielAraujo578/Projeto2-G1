import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options

class SignUpFormTest(unittest.TestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-geolocation")
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            'translate_whitelists': {'YOUR_LANGUAGE_CODE': 'en'}, # Replace YOUR_LANGUAGE_CODE or remove if not needed
            'translate': {'enabled': 'False'}
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-popup-blocking")

        self.driver = webdriver.Chrome(options=chrome_options)

    def test_submit_sign_up_form_successfully(self):
        url = "http://localhost:8000/candidato/cadastro/" 
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        
        user_data_step1 = {
            'name': 'John Doe',
            'date': '2003-05-05',
            'gender': 'Feminino',
            'race': 'Branco',
            'id': '123.456.789-00',
            'telephone': '1234567890',
            'civil': 'Solteiro(a)',
            'email': 'johndoe@gmail.com',
            'password': '1234',
            'confirm_password': '1234',
        }

        driver.get(url)

        input_name = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1-content"]/input[1]'))
        )
        input_name.send_keys(user_data_step1['name'])
        self.assertEqual(input_name.get_attribute("value"), user_data_step1['name'])

        input_date = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1-content"]/input[2]'))
        )
        driver.execute_script("arguments[0].value = arguments[1]", input_date, user_data_step1['date'])
        self.assertEqual(input_date.get_attribute("value"), user_data_step1['date'])

        select_gender_element = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1-content"]/select'))
        )
        select_gender = Select(select_gender_element)
        select_gender.select_by_visible_text(user_data_step1['gender'])
        self.assertEqual(select_gender.first_selected_option.text, user_data_step1['gender'])

        input_race = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1-content"]/input[3]'))
        )
        input_race.send_keys(user_data_step1['race'])
        self.assertEqual(input_race.get_attribute("value"), user_data_step1['race'])

        input_id = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1-content"]/input[4]'))
        )
        input_id.send_keys(user_data_step1['id'])
        self.assertEqual(input_id.get_attribute("value"), user_data_step1['id'])

        input_telephone = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1-content"]/input[5]'))
        )
        input_telephone.send_keys(user_data_step1['telephone'])
        self.assertEqual(input_telephone.get_attribute("value"), user_data_step1['telephone'])

        input_whatsapp = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1-content"]/input[6]'))
        )
        input_whatsapp.click()
        self.assertTrue(input_whatsapp.is_selected() or input_whatsapp.get_attribute("checked"))

        input_civil = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1-content"]/input[7]'))
        )
        input_civil.send_keys(user_data_step1['civil'])
        self.assertEqual(input_civil.get_attribute("value"), user_data_step1['civil'])

        input_email = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1-content"]/input[8]'))
        )
        input_email.send_keys(user_data_step1['email'])
        self.assertEqual(input_email.get_attribute("value"), user_data_step1['email'])

        input_password = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1-content"]/input[9]'))
        )
        input_password.send_keys(user_data_step1['password'])
        self.assertEqual(input_password.get_attribute("value"), user_data_step1['password'])

        input_confirm_password = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1-content"]/input[10]'))
        )
        input_confirm_password.send_keys(user_data_step1['confirm_password'])
        self.assertEqual(input_confirm_password.get_attribute("value"), user_data_step1['confirm_password'])

        next_button_step1 = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="next-btn"]'))
        )
        next_button_step1.click()

        user_data_step2 = {
            'main_address': 'Rua das Palmeiras',
            'number': '789',
            'neighborhood': 'Vila EsperanÃ§a',
            'city_state': 'Curitiba/PR',
            'microregion': 'Metropolitana de Curitiba',
            'zip_code': '80000-123',
            'shift': 'Morning', 
        }

        input_main_address = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-2-content"]/input[1]'))
        )
        input_main_address.send_keys(user_data_step2['main_address'])
        self.assertEqual(input_main_address.get_attribute("value"), user_data_step2['main_address'])

        input_number = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-2-content"]/input[2]')) 
        )
        input_number.send_keys(user_data_step2['number'])
        self.assertEqual(input_number.get_attribute("value"), user_data_step2['number'])

        input_neighborhood = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-2-content"]/input[3]'))
        )
        input_neighborhood.send_keys(user_data_step2['neighborhood'])
        self.assertEqual(input_neighborhood.get_attribute("value"), user_data_step2['neighborhood'])

        input_city_state = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-2-content"]/input[4]'))
        )
        input_city_state.send_keys(user_data_step2['city_state'])
        self.assertEqual(input_city_state.get_attribute("value"), user_data_step2['city_state'])

        input_microregion = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-2-content"]/input[5]'))
        )
        input_microregion.send_keys(user_data_step2['microregion'])
        self.assertEqual(input_microregion.get_attribute("value"), user_data_step2['microregion'])

        input_zip_code = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-2-content"]/input[6]'))
        )
        input_zip_code.send_keys(user_data_step2['zip_code'])
        self.assertEqual(input_zip_code.get_attribute("value"), user_data_step2['zip_code'])

        checkbox_will_enroll = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-2-content"]/input[7]'))
        )
        checkbox_will_enroll.click()
        self.assertTrue(checkbox_will_enroll.is_selected() or checkbox_will_enroll.get_attribute("checked"))

        input_shift = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-2-content"]/input[8]'))
        )
        input_shift.send_keys(user_data_step2['shift'])
        self.assertEqual(input_shift.get_attribute("value"), user_data_step2['shift'])

        checkbox_sponsored = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-2-content"]/input[9]'))
        )
        checkbox_sponsored.click()
        self.assertTrue(checkbox_sponsored.is_selected() or checkbox_sponsored.get_attribute("checked"))

        next_button_step2 = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="next-btn"]'))
        )
        next_button_step2.click()

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()