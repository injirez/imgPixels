from django.shortcuts import render
from .forms import ImageForm
from .models import Image
import time
from django.conf import settings

import cv2
import numpy as np


def imageUploadView(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            imgObj = form.instance
            imageUrl = imgObj.image.url.replace('media', '').replace('/', '\\').replace('\\\\', '\\')
            imageUrl = settings.MEDIA_ROOT.replace('/', '') + imageUrl
            img = cv2.imread(imageUrl, cv2.IMREAD_GRAYSCALE)
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
