"""
vindicta
~~~~~~~~

Did someone take your class and leave you stuck with an 8am Calculus II class
for four days a week over twelve weeks of the Summer college session?
Vindicta is here to help.

:author: Sean Pianka
:github: @seanpianka
:e-mail: pianka@eml.cc

"""
from datetime import datetime
from pprint import pprint
from lxml import html
import requests
import traceback
import time
import random
import json
import logging
import os
import time
import getpass

import argparse
import selenium
import selenium.webdriver.support.ui as ui
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from logger import CustomLogger


logger = CustomLogger(__name__)


class XXXBotEngine(object):
    TIME_FORMAT = r"%Y-%m-%d-%H-%M-%S"
    XXX_LOGIN_URL = "https://cas.xxx.edu/cas/login?service=https://my.xxx.edu"
    DEFAULT_WEBDRIVER_WAIT_TIME = 10

    def __init__(
        self,
        executable_path="",
        xxxid="",
        password="",
        auto_login=False,
        browser="chrome",
        sleep_time=1.5,
        webhook_url="",
        **kwargs,
    ):
        """
        :param driver: Instance of selenium driver already instantiated.
        :param executable_path: Path to the driver/executable to instantiate
            the selenium driver with.
        :param xxxid: XXX-ID to use when logging into MyXXX.
        :param password: Password to use when logging into MyXXX.
        :param use_cli: Decision to look for/make use of provided CLI arguments.
        :param auto_login: Decision to automatically login to MyXXX.
        :param browser: Name of actual browser ('chrome' or 'firefox')
        :param sleep_time: Adjust based on connection speed, time between actions.
        """
        # use_cli = bool(kwargs.get("use_cli", False))
        # **XXXBotEngine.ArgParser().parse_args()

        self.SLEEP_TIME = float(sleep_time)
        self.xxxid = xxxid if xxxid else input("XXX-ID: ")
        self.password = password if password else getpass.getpass()
        self.webhook_url = webhook_url

        FIREFOX_NAMES = ("firefox", "gecko", "geckodriver", "firefoxdriver")
        CHROME_NAMES = ("chrome", "chromedriver", "chromedriver-mac", "googlechrome")

        logger.info(f"Selecting browser: {browser}")

        if browser in FIREFOX_NAMES:
            self.dr = (
                webdriver.Firefox(firefox_binary=FirefoxBinary(executable_path))
                if executable_path
                else webdriver.Firefox()
            )
        elif browser in CHROME_NAMES:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-extensions")

            self.dr = (
                webdriver.Chrome(
                    executable_path=executable_path, options=chrome_options
                )
                if executable_path
                else webdriver.Chrome(options=chrome_options)
            )
        else:
            raise RuntimeError(
                '"No valid webdriver-identifying name provided", bailing.'
            )

        logger.info(f"Loaded browser: {browser}")
        self.WAIT = ui.WebDriverWait(self.dr, XXXBotEngine.DEFAULT_WEBDRIVER_WAIT_TIME)

        if auto_login:
            logger.info("Logging into MyXXX...")

            # swap old wait object with a new wait, extended wait object
            # account for possible ~20 second delay due to password change notification
            old_wait = self.WAIT
            self.WAIT = ui.WebDriverWait(self.dr, 30)

            logger.debug("Navigating to login page...")
            self.dr.get(XXXBotEngine.XXX_LOGIN_URL)

            username = self.find("username", "id")[0]
            password = self.find("password", "id")[0]

            logger.debug("Entering login credentials...")

            username.send_keys(self.xxxid)
            password.send_keys(self.password)

            logger.debug("Clicking login button...")
            self.find("#xxx-login-button", "css-selector")[0].click()

            if (
                self.dr.current_url
                == "https://cas.xxx.edu/cas/login?service=https://my.xxx.edu"
            ):
                self.find('//*[@id="form"]/input[3]', "xpath")[0].click()

            self.find(
                '//*[@id="kgoui_Rcontent_I0_Rcolumns0_I0_Rcontent_I0"]/div/a[2]/img',
                "xpath",
            )
            logger.info("Successfully logged into MyXXX.")

            # restore old wait
            self.WAIT = old_wait

    def click(self, title=None, xpath=None, css_selector=None):
        logger.debug("Clicking on " + title + "...")

        if xpath:
            element = self.find(xpath, "xpath")[0]
        elif css_selector:
            element = self.find(css_selector, "css-selector")[0]
        else:
            raise ValueError(
                "Unable to locate element without xpath or " "css selector."
            )

        element.click()
        logger.debug("Click succeeded.")

    def focus_iframe(self, title, xpath=None, css_selector=None):
        logger.debug(f"Focusing on " + title + "'s i-frame...")

        if xpath:
            frame = self.find(xpath, "xpath")[0]
        elif css_selector:
            frame = self.find(css_selector, "css-selector")[0]
        else:
            raise ValueError(
                "Unable to locate element without xpath or " "css selector."
            )

        self.dr.switch_to.frame(frame)

        logger.debug("i-frame focusing succeeded.")

    def find(self, path, path_type):
        path_finders = {
            "css-selector": self.dr.find_elements_by_css_selector,
            "xpath": self.dr.find_elements_by_xpath,
            "id": self.dr.find_elements_by_id,
        }

        if path_type not in path_finders.keys():
            raise ValueError(f"invalid path type: {path_finders.keys()}")

        self.WAIT.until(lambda driver: path_finders[path_type](path))
        return path_finders[path_type](path)

    @property
    def page_source(self):
        return self.dr.page_source.encode("utf-8")


def now(f=XXXBotEngine.TIME_FORMAT):
    return datetime.now().strftime(f)


if __name__ == "__main__":
    import selenium.webdriver.support.ui as ui
    import boto3

    logger.setLevel(logging.DEBUG)

    def create_bot():
        # ssm = boto3.client("ssm", "us-east-1")
        ssm = boto3.Session(profile_name="sean").client("ssm", "us-east-1")
        response = ssm.get_parameters(Names=["xxx_id", "xxx_pw", "personal_slack_webhook_url"], WithDecryption=True)[
            "Parameters"
        ]

        return XXXBotEngine(
            auto_login=True, xxxid=response[0]["Value"], password=response[1]["Value"], webhook_url=response[2]["Value"]
        )

    bot = create_bot()

    # Navigate to shopping cart
    bot.click(
        title="sc classes button on home page",
        xpath="""//*[@id="kgoui_Rcontent_I0_Rcolumns0_I0_Rcontent_I0"]/div/a[5]/img""",
    )
    bot.click(
        title="my classes button on sc home page",
        xpath="""//*[@id="win0groupletPTNUI_LAND_REC_GROUPLET$7"]""",
    )

    if bot.webhook_url:
        requests.post(
            bot.webhook_url,
            data=json.dumps({'text': f"Vindicta now running..."}),
            headers={'Content-Type': 'application/json'}
        )
    # While there are classes in the shopping cart
    # TODO: Guarantee breaking only in necessary circumstances
    try_counter = 0
    while try_counter < 5:
        try:
            # Refresh shopping cart
            logger.info(f"** REFRESH: {now()}:")
            # unfocus from any currently focused i-frame
            bot.dr.switch_to.default_content()
            bot.click(
                title="Enrollment: Add Classes",
                xpath="""//*[@id="win4divPTGP_STEP_DVW_PTGP_STEP_BTN_GB$5"]"""
            )
            bot.focus_iframe(
                title="term select",
                xpath="""//*[@id="main_target_win0"]"""
            )

            try:
                bot.find("""//*[@id="DERIVED_REGFRM1_LINK_ADD_ENRL$82$"]""", "xpath")
            except selenium.common.exceptions.TimeoutException:
                bot.click(
                    title="2019 spring, radio",
                    xpath="""//*[@id="SSR_DUMMY_RECV1$sels$1$$0"]""",
                )
                bot.click(
                    title="2019 spring, continue",
                    xpath="""//*[@id="DERIVED_SSS_SCT_SSR_PB_GO"]""",
                )

            # Get all courses in the course shopping cart
            shopping_cart_rows = [
                r
                for r in html.fromstring(bot.page_source).xpath(
                    # xpath for all rows in shopping cart, contains title & status
                    # """//*[@id="SSR_REGFORM_VW$scroll$0"]/tbody/tr/td/table/tbody/tr"""
                    """/html/body/form/div[5]/table/tbody/tr/td/div/table/tbody/tr[8]/td[2]/div/table/tbody/tr/td/table/tbody/tr[4]/td[2]/div/table/tbody/tr/td/table/tbody/tr[3]/td[3]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr/td/table/tbody/tr"""
                )[1:]
                if r.getchildren()[1].find(".//a") is not None
            ]

            # Use a "try" if the course shopping cart is empty
            if len(shopping_cart_rows) == 0:
                try_counter += 1
                logger.info("The course shopping cart is empty.")
                continue

            # Cleaned up list of courses
            courses = [
                {
                    "Course": row.getchildren()[1].findall(".//a")[0],
                    "Title": row.getchildren()[1]
                    .findall(".//a")[0]
                    .text_content()
                    .splitlines()[0],
                    "Code": row.getchildren()[1]
                    .findall(".//a")[0]
                    .text_content()
                    .splitlines()[1]
                    .strip()
                    .replace("(", "")
                    .replace(")", ""),
                    "Status": row.getchildren()[-1].findall(".//img")[0].attrib["alt"],
                    "Row": row,
                }
                for row in shopping_cart_rows
            ]

            open_courses = [c["Status"] == "Open" for c in courses]
            logger.info(f"Found {len(courses)} in cart: {sum(open_courses)} Open")

            if any(open_courses):
                if bot.webhook_url:
                    requests.post(
                        bot.webhook_url,
                        data=json.dumps({'text': f"Found {sum(open_courses)} open courses"}),
                        headers={'Content-Type': 'application/json'}
                    )

                bot.click(
                    title="Proceed to Step 2 of 3",
                    xpath='//*[@id="win0divDERIVED_REGFRM1_LINK_ADD_ENRL$82$"]/a',
                )

                bot.click(
                    title="Finish Enrolling",
                    xpath='//*[@id="DERIVED_REGFRM1_SSR_PB_SUBMIT"]',
                )

                # Check if anything worked, otherwise
                try:
                    if (
                        sum(
                            [
                                r.getchildren()[-1].findall(".//img")[0].attrib["alt"]
                                != "Error"
                                for r in html.fromstring(bot.page_source).xpath(
                                    "/html/body/form/div[5]/table/tbody/tr/td/div/table/tbody/tr[9]/td[2]/div/table/tbody/tr/td/table/tbody/tr"
                                )[1:]
                            ]
                        )
                        != 0
                    ):
                        logger.info("Successfully added classes")

                        if bot.webhook_url:
                            requests.post(
                                bot.webhook_url,
                                data=json.dumps({'text': f"Registered for {sum(open_courses)} courses"}),
                                headers={'Content-Type': 'application/json'}
                            )

                        with open('output.log', 'w') as f:
                            f.write(f"Added classes at {now()}")

                    else:
                        logger.error("Failed to add any classes")
                except selenium.common.exceptions.TimeoutException:
                    logger.error("Failed to reach add classes page")

            try_counter = 0

        except Exception as e:
            try_counter += 1
            print(f"Error, skipping... try counter: {try_counter}")
            logger.error(str(e))
            traceback.print_exc()
            continue

        finally:
            sleep_time = random.choice(range(5, 20, 1))
            logger.info(f"Sleeping {sleep_time} seconds...")
            time.sleep(sleep_time)
