from flask import Flask, render_template
from api import get_numbers

app = Flask(__name__)
app.debug = True

@app.route('/'):
def index():
    numbers = get_numbers()
    return render_template('index.html', numbers = numbers)


if __name__ =='__main__':
    app.run()	
    
