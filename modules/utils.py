import configparser
import codecs
import logging
import random

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from fake_useragent import UserAgent


def build_config(config_name='config.ini') -> None:
    """Build default config section key/values"""
    config = configparser.ConfigParser()
    config.update({
        'MAIN': {
            'debug': True,
        },
        'DB': {
            'table': 'scrapers'
        },
        'SENTRY': {
            'dsn': '',
            'log_level': 20
        },
    })
    with open(config_name, 'w') as f:
        print('- Creating new config')
        config.write(f)


def load_config(config_fp='config.ini'):
    """load config from `config_fp`; build default if not found"""
    config = configparser.ConfigParser()
    try:
        config.read_file(codecs.open(config_fp, 'r', 'utf8'))
    except FileNotFoundError:
        print('- Config not found')
        build_config()
        config.read_file(codecs.open(config_fp, 'r', 'utf8'))
    return config


def handle_error(error, to_file=False, to_file_path='error_log.txt'):
    """Handle error by writing to file/sending to sentry/raising"""
    if to_file:
        with open(to_file_path, 'a', encoding='utf-8') as f:
            f.write(error + '\n')
    else:
        raise error


def load_proxies(filename='proxies.txt'):
    """Load proxies from local file"""
    proxies = []
    try:
        with open(filename, 'r') as file:
            proxies_raw = file.readlines()
            for line in proxies_raw:
                proxies.append(line.strip().split(':'))
        return proxies
    except FileNotFoundError:
        logging.warning(f'Proxy file: {filename} not found')
        return proxies
    except Exception as e:
        handle_error(e)


def proxy_build_rotate(proxies: list, protocol='') -> str:
    """Build http/https proxy for list of proxies"""
    proxy_index = random.randint(0, len(proxies) - 1)
    proxy = proxies[proxy_index]
    if protocol:
        proxy = f'{protocol}://{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}'
    else:
        proxy = f'{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}'
    print('- Proxy: ', proxy)
    return proxy


def setup_user_agent() -> str:
    """Generate user_agent string"""
    user_agent = UserAgent()
    return user_agent.random


def setup_selenium_proxy(proxy: str) -> dict:
    """Setup http proxy for selenium"""
    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': proxy,
        'sslProxy': 'https://' + proxy,
        'noProxy': ''})
    capabilities = webdriver.DesiredCapabilities.CHROME
    proxy.add_to_capabilities(capabilities)
    return capabilities
