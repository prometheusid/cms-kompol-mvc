from flask import Flask

app = Flask("project")


from project.controllers.auth import *
from project.controllers.pub import *
from project.controllers.panel import *
