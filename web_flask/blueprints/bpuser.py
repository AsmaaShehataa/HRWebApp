#!/usr/bin/python3
"""Blue print for User"""

from flask import Blueprint

bpuser = Blueprint('bpuser', __name__, url_prefix='/HrWeb/user')

# Example route
@bpuser.route('/example')
def example():
    return "This is an example route!"
