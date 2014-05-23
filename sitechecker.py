#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import smtplib
import argparse
from os import sys
import traceback
import logging

class Browser(object):
    
    def __init__(self, logger):
        logger.info("Starting browser")
        self.browser = webdriver.Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.FIREFOX)
    
    def get(self, url, logger):
        logger.info("Browser is getting %s" % url)
        self.browser.get(url)

    def close(self, logger):
        logger.info("Closing the browser")
        self.browser.close()

    def title(self, logger):
        logger.info("Getting the current page title")
        return self.browser.title

class Email(object):

    def __init__(self, fromemail, password, toemail, message, logger):

        self.fromemail = fromemail
        self.password = password
        self.toemail = toemail
        self.message = message
        logger.info("Creating new email")
        logger.info("From email: %s" % self.fromemail)
        logger.info("To email: %s" % self.toemail)
        logger.info("Message: %s" % self.message)

    def send_fail_message(self, logger):
        server = smtplib.SMTP("smtp.gmail.com:587")
        logger.info("smpt server set to: smtp.gmail.com:587")
        server.starttls()
        logger.info("logging into smpt server")
        server.login(self.fromemail, self.password)
        logger.info("sending email")
        server.sendmail(self.fromemail, self.toemail, "\n" + self.message)

class Site(object):

    def __init__(self, url, title, logger):

        self.url = url
        self.title = title
        self.valid = None
        logger.info("New site object")
        logger.info("URL: %s" % self.url)
        logger.info("Expected title: %s" % self.title)
    
    def check(self, driver, logger):

        driver.get(self.url, logger)
        try:
            assert self.title in driver.title(logger)
            valid = True
        except AssertionError as ae:
            valid = False

def setup_logger(log_filename):

    # Setup logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    # create a file handler
    handler = logging.FileHandler(log_filename)
    handler.setLevel(logging.INFO)
    # create a logging format
    formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(message)s')
    handler.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(handler)
    
    return logger

def parse_args(args):
    """Takes command line arguments and processes them

    -u		--url			<string>	"http://area515.org"
    -t		--title			<string>	"Des Moines Makerspace"
    -f		--fromemail		<string>	"somebot@email.com"
    -p		--password		<string>	"somebotspassword"
    -to		--toemail		<string>	"persontoalert@gmail.com"
    -lo		--log			<string>	"sitechecker-area515.log
    
    """
    
    parser = argparse.ArgumentParser(prefix_chars='-')
    
    parser.add_argument('-u', '--url', type=str)
    parser.add_argument('-t', '--title', type=str)
    parser.add_argument('-f', '--fromemail', type=str)
    parser.add_argument('-p', '--password', type=str)
    parser.add_argument('-to', '--toemail', type=str)
    parser.add_argument('-lo', '--log', type=str)

    parsed_args, unknown = parser.parse_known_args(args)

    return parsed_args


def main():
    """Parse the command line config and check the site.
    """
    args = parse_args(sys.argv)
    logger = setup_logger(args.log)
    browser = Browser(logger)

    site = Site(args.url, args.title,logger)
    try:
        site.check(browser,logger)
    except:
        print traceback.format_exc()
    finally:
        if not site.valid:
            message = "Unable to contact %s" % site.url
            alert = Email(args.fromemail, args.password, args.toemail, message, logger)
            alert.send_fail_message(logger)

    if browser is not None:
        browser.close(logger)
    logger.info("Completed testing the site")


if __name__ == "__main__":
    main()
