# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 11:42:14 2021

@author: nadee
"""

from app import app
port = int(os.environ.get("PORT", 5000))
app.run(debug = False,host='0.0.0.0', port=port) #port = 8000
#app.run(debug=True)


