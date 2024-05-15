import pytest
import sqlite3
import time
from selenium import webdriver

from pathlib import Path

@pytest.fixture
def URL():
    return 'http://127.0.0.1:5000' # URL of the program


@pytest.fixture
def driver():
    return webdriver.Edge()  # follow the "End-to-end testing" section in README.md to install the web driver executable


@pytest.fixture
def restore_sqlite_database():
    '''
    Automatically restore SQLite database file app/db/wordfreqapp.db
    using SQL statements from app/static/wordfreqapp.sql
    '''
    con = sqlite3.connect('../db/wordfreqapp.db')
    with con:
        con.executescript('DROP TABLE IF EXISTS user;')
        con.executescript('DROP TABLE IF EXISTS article;')
        con.executescript(open('../static/wordfreqapp.sql', encoding='utf8').read())
    con.close()


@pytest.fixture(autouse=True)
def restart_englishpal(restore_sqlite_database):
    (Path(__file__).parent / '../main.py').touch()
    time.sleep(1)
