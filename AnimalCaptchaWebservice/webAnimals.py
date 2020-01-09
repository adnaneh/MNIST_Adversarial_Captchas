from flask import Flask, make_response, render_template, request,url_for,redirect
import os
import random
import pathlib
import shutil
import time
import numpy as np

app = Flask(__name__)
data_path = 'delta=255'
doc_form = '.bmp'
translate = {"0": "dog", "1": "horse", "2": "elephant", "3": "butterfly", "4": "chicken", "5": "cat", "6": "cow", "7": "sheep", "8": "spider", "9": "squirrel"}

def clear_static():
    files = os.listdir('./static/')
    for f in files:
        os.remove('./static/' + f)


def random_img(collection, cover):
    root_dir = os.path.abspath(os.path.dirname(__file__))
    # answer = os.listdir(root_dir + 'static')[0][-8:-4]
    img_path = root_dir + '\\' + data_path + '\\' + collection
    files = os.listdir(img_path)
    img = img_path + "\\" + files[random.randint(0, len(files) - 1)]
    shutil.copy(img, root_dir + '\static\\' + cover + doc_form)

def random_imgs(img_n):
    objectifs = os.listdir('./' + data_path)
    objectif = objectifs[random.randint(0, len(objectifs) - 1)]
    objectifs.remove(objectif)

    indices = list(range(img_n))
    np.random.shuffle(indices)
    obj_n = random.randint(1,img_n//2)
    for i in range(obj_n):
        random_img(objectif, str(indices[i]))
    for i in indices[obj_n:img_n]:
        random_img(objectifs[random.randint(0, len(objectifs) - 1)], str(i))

    return indices[0:obj_n], translate[objectif]

@app.route('/')
def captcha():
    return 'common index'


@app.route('/graph_captcha/', methods=['GET', 'POST'])
def graph_captcha():
    name = ''
    if request.method == 'GET':
        global answers
        answers, name = random_imgs(9)
    elif request.method == 'POST':
        for index in range(9):
            if (index in answers and request.form.get(str(index)) is None) or (index not in answers and request.form.get(str(index)) is not None):
                retry_url = url_for('retry')
                return redirect(retry_url)

        clear_static()
        success_url = url_for('success')
        return redirect(success_url)

    return render_template('homepage.html', target= name, val1=time.time(), doc=doc_form)


@app.route('/retry/', methods=['GET', 'POST'])
def retry():
    name = ''
    if request.method == 'GET':
        global answers
        answers, name = random_imgs(9)
    elif request.method == 'POST':
        for index in range(9):
            if (index in answers and request.form.get(str(index)) is None) or (
                    index not in answers and request.form.get(str(index)) is not None):
                retry_url = url_for('retry')
                return redirect(retry_url)

        clear_static()
        success_url = url_for('success')
        return redirect(success_url)

    return render_template('wrong.html', target=name, val1=time.time(),doc=doc_form)


@app.route('/success/', methods=['GET', 'POST'])
def success():
    if request.method == 'POST':
        home_url = url_for('graph_captcha')
        return redirect(home_url)
    return render_template('success.html')


if __name__ == '__main__':

    app.run(debug=True, port=4000)
