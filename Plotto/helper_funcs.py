from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import logging
import random
import json
from typing import List, Dict

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


# logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
#                   level=logging.INFO)  # For logging to console, Debugging purposes.

def load_names(file_path: str) -> Dict[str, List[str]]:
    """Load male and female names from a JSON file."""
    with open(file_path, "r") as file:
        return json.load(file)

def load_gender_map(file_path: str) -> Dict[str, str]:
    """Load the gender map from a JSON file."""
    with open(file_path, "r") as file:
        return json.load(file)

def load_pronoun_map(file_path: str) -> Dict[str, Dict[str, str]]:
    """Load the pronoun map from a JSON file."""
    with open(file_path, "r") as file:
        return json.load(file)

# function to pick random caluse
def random_clause(arr):
    """Select a random clause from a list.
    Parameters:arr (list): A list of items to choose from.
    Returns:Any: A randomly selected item from the list, or None if the list is empty."""
    if not arr:
        return None
    return random.choice(arr)

def random_name(character_symbol: str, gender: str,
                 male_names: List[str], female_names: List[str]) -> str:
    """Generate a random name based on gender."""
    if gender == 'male':
        names = male_names
    elif gender == 'female':
        names = female_names
    elif gender == 'any':
        names = male_names if random.random() < 0.5 else female_names
    else:
        return character_symbol

    if names:
        name = names.pop(random.randint(0, len(names) - 1))
        return name
    return character_symbol


class HelperFn:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, xpath, timeout=22):
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            logging.info("# Element '%s' is present." % xpath)
        except TimeoutException:
            logging.error("# Element '%s' is not present." % xpath)

    def is_element_present(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
            logging.info("# Element '%s' is present." % xpath)
        except NoSuchElementException:
            logging.error("# Element '%s' is not present." % xpath)
            return False
        return True

    def wait_for_element_visible(self, xpath, timeout=22):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            logging.info("# Element '%s' is visible." % xpath)
        except TimeoutException:
            logging.error("# Element '%s' is not visible." % xpath)

    def is_element_visible(self, xpath):
        try:
            logging.info("# Element '%s' is visible." % xpath)
            return self.driver.find_element(By.XPATH, xpath).is_displayed()
        except NoSuchElementException:
            logging.error("# Element '%s' is not visible." % xpath)
            return False

    def find_element(self, xpath):
        try:
            element = self.driver.find_element(By.XPATH, xpath)
            logging.info("# Element '%s' is found." % xpath)
        except NoSuchElementException:
            logging.error("# Element '%s' is not found." % xpath)
            return False
        return element

    def find_elements(self, xpath):
        try:
            elements = self.driver.find_elements(By.XPATH, xpath)
            logging.info("# Element '%s' is found." % xpath)
        except NoSuchElementException:
            logging.error("# Element '%s' is not found." % xpath)
            return False
        return elements

    def wait_for_x_seconds(self, seconds):
        logging.info("# Waiting for %s seconds." % seconds)
        self.driver.implicitly_wait(seconds)
        logging.info("# Done waiting for %s seconds." % seconds)