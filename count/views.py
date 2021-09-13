from django.shortcuts import render
from .forms import ImageForm
from .models import Image
import time
from django.conf import settings

import cv2
import numpy as np
import urllib.request


def imageUploadView(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            imgObj = form.instance

            # FOR LOCAL
            imageUrl = imgObj.image.url.replace('media', '').replace('/', '\\')
            imageUrl = settings.MEDIA_ROOT.replace('/', '') + imageUrl
            img = cv2.imread(imageUrl, cv2.IMREAD_GRAYSCALE)

            # FOR HEROKU
            # imageUrlHeroku = 'https://imgpixels.herokuapp.com' + imgObj.image.url
            # resp = urllib.request.urlopen(imageUrlHeroku)
            # image = np.asarray(bytearray(resp.read()), dtype="uint8")
            # img = cv2.imdecode(image, cv2.IMREAD_COLOR)

            numWhite = np.sum(img == 255)
            numBlack = np.sum(img == 0)
            if numWhite > numBlack:
                res = 'Number of white pixels is more then black pixels ({})'.format(numWhite)
            elif numWhite < numBlack:
                res = 'Number of black pixels is more then white pixels ({})'.format(numBlack)
            elif numBlack == numWhite:
                res = 'Number of pixels is same'
            return render(request, 'index.html', {'form': form, 'img_obj': imgObj, 'numWhite': numWhite, 'numBlack': numBlack, 'res': res})
    else:
        form = ImageForm()
    return render(request, 'index.html', {'form': form})
