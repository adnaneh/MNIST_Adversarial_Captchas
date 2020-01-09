import requests
import matplotlib.pyplot as plt
import cv2
from keras.models import load_model
import numpy as np
import torchvision.transforms as transforms
import torch
from PIL import Image

ind_to_name = {"0": "dog", "1": "horse", "2": "elephant", "3": "butterfly", "4": "chicken",
               "5": "cat", "6": "cow", "7": "sheep", "8": "spider", "9": "squirrel"}

# Check for cuda devices
device = 'cuda' if torch.cuda.is_available() else 'cpu'
net = torch.load('./MODELS/animals10_resnet18.pth', map_location=torch.device('cpu'))
net = net.to(device)
net.eval()

k = 0
for j in range(100):

    dummy = requests.get("http://127.0.0.1:4000/graph_captcha/")
    if dummy.status_code != 200:
        exit()
    target_class = dummy.text.split()[14][:-6]

    images = []
    for i in range(0,9):
        images.append(requests.get('http://127.0.0.1:4000/static/./{0}.bmp'.format(i), stream=True))

        with open('{0}.bmp'.format(i), 'wb') as handle:
            for block in images[i].iter_content(1024):
                if not block:
                    break

                handle.write(block)

    print(target_class)
    images = []
    for i in range(0,9):
        image = Image.open('{0}.bmp'.format(i))
        images.append(image)


    data_inputs = {}
    for i,image in enumerate(images):
        image = transforms.ToTensor()(image)
        image = image[None, :, :, :].to(device)
        label = torch.argmax(net.forward(torch.autograd.Variable(image, requires_grad=True)).data).item()
        label = ind_to_name[str(label)]

        if label == target_class:
            data_inputs[i] = i

    response = requests.post("http://127.0.0.1:4000/graph_captcha/",
                             data=data_inputs)

    if "SUCCESS" in response.text:
        k = k + 1

print("The accuracy of attacks was")
print(k/j)