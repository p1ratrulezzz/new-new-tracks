from src.storage.jsonstorage import JsonStorage
from constants import *
from src.formatter.htmlformatter import HtmlFormatter

storage = JsonStorage(filename = JSON_FILENAME)

# Build index.html
formatter_html = HtmlFormatter(storage)
formatter_html.render('docs/index.html')