import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

class SignUpFormTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
    
    def test_submit_sign_up_form_successfully(self):
        url = "localhost:8000/candidato/cadastro/"
        driver = self.driver                            
        wait = WebDriverWait(driver, 10)
        user_data = {
            'name': 'John Doe',
            'date': '05/05/2003',
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
        input_name.send_keys(user_data['name'])

        input_date = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1-content"]/input[2]'))
        )
        input_date.send_keys(user_data['date'])
    
        select_gender_element = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1-content"]/select'))
        )
        select_gender = Select(select_gender_element)
        select_gender.select_by_visible_text(user_data['gender'])

        input_race = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1-content"]/input[3]'))
        )
        input_race.send_keys(user_data['race'])

        input_id = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1-content"]/input[4]'))
        )
        input_id.send_keys(user_data['id'])

        input_telephone = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1-content"]/input[5]'))
        )
        input_telephone.send_keys(user_data['telephone'])

        input_whatsapp = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1-content"]/input[6]'))
        )
        input_whatsapp.click()

        input_civil = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1-content"]/input[7]'))
        )
        input_civil.send_keys(user_data['civil'])

        input_email = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1-content"]/input[8]'))
        )
        input_email.send_keys(user_data['email'])

        input_password = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1-content"]/input[9]'))
        )
        input_password.send_keys(user_data['password'])

        input_confirm_password = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1-content"]/input[10]'))
        )
        input_confirm_password.send_keys(user_data['confirm_password'])

        next_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="next-btn"]'))
        )
        next_button.click()

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()