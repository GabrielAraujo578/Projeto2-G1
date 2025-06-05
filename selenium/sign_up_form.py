import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

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
            'translate_whitelists': {'YOUR_LANGUAGE_CODE': 'en'},
            'translate': {'enabled': 'False'}
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-popup-blocking")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
    def tearDown(self):
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

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

        user_data_step3 = {
            'education': 'Ensino médio incompleto',
            'school': 'Escola Estadual de Ensino Médio',
            'grade': '3 ano',
            'school shift': 'Manhã',
            'reason': 'Preciso de uma oportunidade para melhorar minha situação financeira.',
            'employment status': 'Trabalhando', 
            'job': 'Assistente Administrativo',
            'job_location': 'Curitiba/PR',
            'job_neighborhood': 'Centro',
            'job_salary': '150000'
        }

        input_education = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-3-content"]/input[1]'))
        )
        input_education.send_keys(user_data_step3['education'])
        self.assertEqual(input_education.get_attribute("value"), user_data_step3['education'])

        input_school = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-3-content"]/input[2]'))
        )
        input_school.send_keys(user_data_step3['school'])
        self.assertEqual(input_school.get_attribute("value"), user_data_step3['school'])

        input_grade = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-3-content"]/input[3]'))
        )
        input_grade.send_keys(user_data_step3['grade'])
        self.assertEqual(input_grade.get_attribute("value"), user_data_step3['grade'])

        input_school_shift = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-3-content"]/input[4]'))
        )
        input_school_shift.send_keys(user_data_step3['school shift'])
        self.assertEqual(input_school_shift.get_attribute("value"), user_data_step3['school shift'])

        input_reason = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-3-content"]/input[5]'))
        )
        input_reason.send_keys(user_data_step3['reason'])
        self.assertEqual(input_reason.get_attribute("value"), user_data_step3['reason'])


        checkbox_study_plans = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-3-content"]/input[6]'))
        )
        checkbox_study_plans.click()
        self.assertTrue(checkbox_study_plans.is_selected() or checkbox_study_plans.get_attribute("checked"))


        input_employment_status = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-3-content"]/input[7]'))
        )
        input_employment_status.send_keys(user_data_step3['employment status'])
        self.assertEqual(input_employment_status.get_attribute("value"), user_data_step3['employment status'])

        input_job = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-3-content"]/input[8]'))
        )
        input_job.send_keys(user_data_step3['job'])
        self.assertEqual(input_job.get_attribute("value"), user_data_step3['job'])

        input_job_loacation = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-3-content"]/input[9]'))
        )
        input_job_loacation.send_keys(user_data_step3['job_location'])
        self.assertEqual(input_job_loacation.get_attribute("value"), user_data_step3['job_location'])

        input_job_neighborhood = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-3-content"]/input[10]'))
        )
        input_job_neighborhood.send_keys(user_data_step3['job_neighborhood'])
        self.assertEqual(input_job_neighborhood.get_attribute("value"), user_data_step3['job_neighborhood'])

        input_job_salary = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-3-content"]/input[11]'))
        )
        input_job_salary.send_keys(user_data_step3['job_salary'])
        self.assertEqual(input_job_salary.get_attribute("value"), user_data_step3['job_salary'])

        next_button_step3 = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="next-btn"]'))
        )
        next_button_step3.click()

        user_data_step4 = {
            'health_insurance': 'Hapvida',
            'health_complaint': 'Nenhuma',
            'deficiency': 'Nenhuma',
            'mental_development': 'Nenhuma',
            'health_improvements': 'Nenhuma',
            'meals': '3',
            'diet': 'Frutas e verduras',
        }

        checkbox_health = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-4-content"]/input[1]'))
        )
        checkbox_health.click()
        self.assertTrue(checkbox_health.is_selected() or checkbox_health.get_attribute("checked"))

        input_health_insurance = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-4-content"]/input[2]'))
        )
        input_health_insurance.send_keys(user_data_step4['health_insurance'])
        self.assertEqual(input_health_insurance.get_attribute("value"), user_data_step4['health_insurance'])

        checkbox_health_problem = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-4-content"]/input[3]'))
        )
        checkbox_health_problem.click()
        self.assertTrue(checkbox_health_problem.is_selected() or checkbox_health_problem.get_attribute("checked"))

        checkbox_medical_care = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-4-content"]/input[4]'))
        )
        checkbox_medical_care.click()
        self.assertTrue(checkbox_medical_care.is_selected() or checkbox_medical_care.get_attribute("checked"))

        checkbox_surgery = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-4-content"]/input[5]'))
        )
        checkbox_surgery.click()
        self.assertTrue(checkbox_surgery.is_selected() or checkbox_surgery.get_attribute("checked"))

        input_health_complaint = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-4-content"]/input[6]'))
        )
        input_health_complaint.send_keys(user_data_step4['health_complaint'])
        self.assertEqual(input_health_complaint.get_attribute("value"), user_data_step4['health_complaint'])

        input_deficiency = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-4-content"]/input[7]'))
        )
        input_deficiency.send_keys(user_data_step4['health_complaint'])
        self.assertEqual(input_health_complaint.get_attribute("value"), user_data_step4['health_complaint'])

        input_mental = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-4-content"]/input[8]'))
        )
        input_mental.send_keys(user_data_step4['mental_development'])
        self.assertEqual(input_mental.get_attribute("value"), user_data_step4['mental_development'])

        input_health_improvements = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-4-content"]/input[9]'))
        )
        input_health_improvements.send_keys(user_data_step4['health_improvements'])
        self.assertEqual(input_health_improvements.get_attribute("value"), user_data_step4['health_improvements'])

        input_meals = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='step-4-content']/input[11]"))
        )
        input_meals.send_keys(Keys.NUMPAD3)
        self.assertEqual(input_meals.get_attribute("value"), user_data_step4['meals'])

        input_diet = wait.until(
            EC.visibility_of_element_located((By.NAME, "alimentacao"))
        )
        input_diet.send_keys(user_data_step4['diet'])
        self.assertEqual(input_diet.get_attribute("value"), user_data_step4['diet'])

        next_button_step4 = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="next-btn"]'))
        )
        next_button_step4.click()

        user_data_step5 = {
            'house': 'Casa',
            'housing': 'Familiar',
            'vulnerability': '',
            'rooms': '3',
            'water': 'Nenhuma',
            'garbage': 'Melhorar a frequência dos ônibus.',
            'sewage': 'Melhorar a frequência dos ônibus.',
            'assets': 'Nenhum',
            'assets_origin': 'Doação',
            'household': '2000',
            'income': '150000',
            'comunity': 'Não',
            'ECA': 'Sim',
            'family': 'Mãe',
            'council': 'Não',
            'FOSCAR': 'Não',
            'guardian_name': 'Maria da Silva',
            'guardian_id': '987.654.321-00',
            'guardian_birthdate': '1208-01-01'
        }

        input_house = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[1]'))
        )
        input_house.send_keys(user_data_step5['house'])
        self.assertEqual(input_house.get_attribute("value"), user_data_step5['house'])

        input_housing = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[2]'))
        )
        input_housing.send_keys(user_data_step5['housing'])
        self.assertEqual(input_housing.get_attribute("value"), user_data_step5['housing'])

        input_vulnerability = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[3]'))
        )
        input_vulnerability.send_keys(user_data_step5['vulnerability'])
        self.assertEqual(input_vulnerability.get_attribute("value"), user_data_step5['vulnerability'])

        input_rooms = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[4]'))
        )
        input_rooms.send_keys(user_data_step5['rooms'])
        self.assertEqual(input_rooms.get_attribute("value"), user_data_step5['rooms'])

        checkbox_child_adult = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[5]'))
        )
        checkbox_child_adult.click()
        self.assertTrue(checkbox_child_adult.is_selected() or checkbox_child_adult.get_attribute("checked"))

        checkbox_bathroom = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[6]'))
        )
        checkbox_bathroom.click()
        self.assertTrue(checkbox_bathroom.is_selected() or checkbox_bathroom.get_attribute("checked"))

        checkbox_insidebathroom = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[7]'))
        )
        checkbox_insidebathroom.click()
        self.assertTrue(checkbox_insidebathroom.is_selected() or checkbox_insidebathroom.get_attribute("checked"))

        checkbox_energy = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[8]'))
        )
        checkbox_energy.click()
        self.assertTrue(checkbox_energy.is_selected() or checkbox_energy.get_attribute("checked"))

        input_water = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[9]'))
        )
        input_water.send_keys(user_data_step5['water'])
        self.assertEqual(input_water.get_attribute("value"), user_data_step5['water'])

        input_garbage = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[10]'))
        )
        input_garbage.send_keys(user_data_step5['garbage'])
        self.assertEqual(input_garbage.get_attribute("value"), user_data_step5['garbage'])

        input_sewage = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[11]'))
        )
        input_sewage.send_keys(user_data_step5['sewage'])
        self.assertEqual(input_sewage.get_attribute("value"), user_data_step5['sewage'])

        input_assets = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[12]'))
        )
        input_assets.send_keys(user_data_step5['assets'])
        self.assertEqual(input_assets.get_attribute("value"), user_data_step5['assets'])

        input_assets_origin = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[13]'))
        )
        input_assets_origin.send_keys(user_data_step5['assets_origin'])
        self.assertEqual(input_assets_origin.get_attribute("value"), user_data_step5['assets_origin'])

        checkbox_cadunico = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[14]'))
        )
        checkbox_cadunico.click()
        self.assertTrue(checkbox_cadunico.is_selected() or checkbox_cadunico.get_attribute("checked"))

        checkbox_bolsafamilia = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[15]'))
        )
        checkbox_bolsafamilia.click()
        self.assertTrue(checkbox_bolsafamilia.is_selected() or checkbox_bolsafamilia.get_attribute("checked"))

        checkbox_auxilio = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[16]'))
        )
        checkbox_auxilio.click()
        self.assertTrue(checkbox_auxilio.is_selected() or checkbox_auxilio.get_attribute("checked"))

        checkbox_bpc = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[17]'))
        )
        checkbox_bpc.click()
        self.assertTrue(checkbox_bpc.is_selected() or checkbox_bpc.get_attribute("checked"))

        input_household = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[18]'))
        )
        input_household.send_keys(user_data_step5['household'])
        self.assertEqual(input_household.get_attribute("value"), user_data_step5['household'])

        input_income = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[19]'))
        )
        input_income.send_keys(user_data_step5['income'])
        self.assertEqual(input_income.get_attribute("value"), user_data_step5['income'])

        input_comunity = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[20]'))
        )
        input_comunity.send_keys(user_data_step5['comunity'])
        self.assertEqual(input_comunity.get_attribute("value"), user_data_step5['comunity'])

        input_eca = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[21]'))
        )
        input_eca.send_keys(user_data_step5['ECA'])
        self.assertEqual(input_eca.get_attribute("value"), user_data_step5['ECA'])

        checkbox_citizenship = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[22]'))
        )
        checkbox_citizenship.click()
        self.assertTrue(checkbox_citizenship.is_selected() or checkbox_citizenship.get_attribute("checked"))

        input_family = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[23]'))
        )
        input_family.send_keys(user_data_step5['family'])
        self.assertEqual(input_family.get_attribute("value"), user_data_step5['family'])

        input_council = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[24]'))
        )
        input_council.send_keys(user_data_step5['council'])
        self.assertEqual(input_council.get_attribute("value"), user_data_step5['council'])

        input_FOSCAR = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[25]'))
        )
        input_FOSCAR.send_keys(user_data_step5['FOSCAR'])
        self.assertEqual(input_FOSCAR.get_attribute("value"), user_data_step5['FOSCAR'])

        input_guardian_name = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[26]'))
        )
        input_guardian_name.send_keys(user_data_step5['guardian_name'])
        self.assertEqual(input_guardian_name.get_attribute("value"), user_data_step5['guardian_name'])

        input_guardian_id = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[27]'))
        )
        input_guardian_id.send_keys(user_data_step5['guardian_id'])
        self.assertEqual(input_guardian_id.get_attribute("value"), user_data_step5['guardian_id'])
        
        input_guardian_datebirth = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-5-content"]/input[28]'))
        )
        driver.execute_script("arguments[0].value = arguments[1]", input_guardian_datebirth, user_data_step5['guardian_birthdate'])
        self.assertEqual(input_guardian_datebirth.get_attribute("value"), user_data_step5['guardian_birthdate'])

        submit_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="submit-btn"]'))
        )
        submit_button.click()
    
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()