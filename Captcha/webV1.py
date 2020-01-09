from flask import Flask, make_response, render_template, request,url_for
import os
import random
import pathlib
import shutil
import time

# Declare the flask app for the webservice
app = Flask(__name__)
app.debug = True


"""
    This function selects a random Captcha from the given database
    It starts by finding the root directory of this folder
    Them selecting the proper database folder 
    From this database folder we get a random image
    Extract the Captcha answer from the name
    And copy the file into static with a different name
"""
def random_img(database_name='DATABASE'):
    if database_name is None or database_name == "None":
        database_name='DATABASE'

    root_dir = os.path.abspath(os.path.dirname(__file__))
    img_path = root_dir + "/" + database_name

    # If a bad Database name was supplied in the request just return a normal Captcha
    try:
        files = os.listdir(img_path)
    except:
        files = os.listdir(root_dir + "/" + "DATABASE")
        img_path = root_dir + "/" + "DATABASE"

    img = img_path + "\\" + files[random.randint(0, len(files) - 1)]
    global answer
    answer = img[-8:-4]
    shutil.copy(img, root_dir + '\static\\' + 'captcha.png')

@app.route('/')
def index():
    return 'common index'

"""
    Here we have the main server!
    The databased to be used come as a request argument from the URL
"""
@app.route('/digit_captcha', methods=['GET', 'POST'])
def digit_captcha():
    # For get method just get the Captcha and serve it based on the requested database
    if request.method == 'GET':
        database = request.args.get("database")
        random_img(database)
        return render_template('chomepage.html', file=url_for('static', filename='./' + 'captcha.png', _t=time.time())
                               , database=database)

    # If the method is POST just check the requests args
    # If the refresh button was pressed, status will be given refresh and we just refresh the Captcha
    # If there is no answer and the status is not refresh just return the homepage
    elif request.method == 'POST':


        database = request.args.get("database")
        user_input = request.form.get("name")
        status = request.form.get("submit_button")

        #detect if the user has pressed refresh!
        if status == "refresh" or answer is None:
            random_img(database)
            return render_template('chomepage.html',
                                   file=url_for('static', filename='./' + 'captcha.png', _t=time.time())
                                   , database=database)

        # Here if the user input is equal to the registered answer we show them a success page!
        # If they are different just show the failure page!
        if user_input == answer:
            return render_template('csuccess.html', database=database)
        else:
            random_img(database)
            return render_template('cwrong.html', file= url_for('static', filename= './' + 'captcha.png', _t=time.time())
                                   , database=database)


if __name__ == "__main__":

    app.run(port=5050)
