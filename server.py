#Project Flask MVC

__author__ = "indhifarhandika"
__version__ = "1"
__email__ = "indhifarhandika@gmail.com"

from project import app
from flask_ngrok import run_with_ngrok

# Kalau mau run ke ngrok
# run_with_ngrok(app)
if __name__ == '__main__':
    # app.run(host="localhost", port=8000, debug=True)
    app.run()