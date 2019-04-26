# -*- coding: utf-8 -*-
from flask import Blueprint

url = Blueprint('mock-server',__name__)

from . import defView, mockView, localView