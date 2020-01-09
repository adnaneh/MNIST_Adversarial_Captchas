import requests
import matplotlib.pyplot as plt
import cv2
from keras.models import load_model
import numpy as np

"""
    Load the Model to be used to solve the Captchas!
    And the filter
    And the Database!
"""
model_choice = "LeNet"
noise_filter = "Median"
database = "100_FILTER_HYBRID"
verbose = False
if model_choice == "DP":
    model = load_model("./MODELS/captcha_model.hdf5")
elif model_choice == "LeNet":
    model = load_model("./MODELS/LeNet_MNIST_data.hdf5")
elif model_choice == "DP Adversarial" :
    model = load_model("./MODELS/adversarial_captcha_model.hdf5")
elif model_choice == "LeNet Median":
    model = load_model("./MODELS/LeNet_Median_Filter.hdf5")
elif model_choice == "ResNet":
    model = load_model("./MODELS/ResNet_MNIST.hdf5")
elif model_choice == "LeNet Adversarial":
    model = load_model("./MODELS/LeNet_Adversarial_Training.hdf5")
else:
    exit()

k = 0
for j in range(100):
    with open('pic1.jpg', 'wb') as handle:

        dummy = requests.get("http://127.0.0.1:5050/digit_captcha?database={0}".format(database))
        if dummy.status_code != 200:
            exit()
        response = requests.get('http://127.0.0.1:5050/static/./captcha.png', stream=True)

        if not response.ok:
            print(response.status_code)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

    img = cv2.imread('pic1.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if verbose == True:
        plt.imshow(img)
        plt.show()

    """
        Here we have the addition og noise removing filters
        Let's see how the model performs under the condition of noise removal
    """
    if noise_filter == "Blur":
        img = cv2.blur(img,(3,3))
    elif noise_filter == "Gaussian":
        img = cv2.GaussianBlur(img, (3,3), 0)
    elif noise_filter == "Median":
        img = cv2.medianBlur(img, 3)
    else:
        pass


    predicted_captcha = []
    x = 0
    while x != 112:

        while x != 112:
            letter_image = img[0:28, x:x + 28]
            x = x + 28

            # Prepare the data for the deep learning model
            letter_image = 255 - letter_image
            letter_image = letter_image / 255
            letter_image = letter_image.reshape((1, 28, 28, 1))

            predictions = model.predict(letter_image)
            predicted_captcha.append(np.argmax(predictions))

    predicted_captcha = [str(i) for i in predicted_captcha]

    captcha_solution = { 'name': "".join(predicted_captcha) }
    response = requests.post("http://127.0.0.1:5050/digit_captcha?database='{0}'".format(database), data=captcha_solution)

    print(captcha_solution)
    if "SUCCESS" in response.text:
        k = k + 1

print("The accuracy of attacks was")
print(k/j)