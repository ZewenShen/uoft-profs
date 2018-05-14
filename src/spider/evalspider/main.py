import sys
sys.path.append('../util/')
import Database
import json
import requests
import re
from urllib.parse import urlencode
from bs4 import BeautifulSoup

DB_NAME = 'uoftevals'
DB_PATH = '../../../database.info'
