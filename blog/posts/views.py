from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
# Create your views here.
from crowdnet import *
from crowdnet.datautils import load_image, resize_img, preprocess_transform


def index(request):
    return render(request, "index.html")
def image1(request):
    return render(request, "image1.html")
def upload(request):
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)

        img = load_image(args.img_path)
        img, resize_ratio = resize_img(img)

        img_input = preprocess_transform(img).unsqueeze(dim=0)
        pred_density_map = model(img_input).detach().cpu().numpy()[0][0]

        pred_count = count_from_density_map(pred_density_map)

        return render(request, 'upload.html', {'file_url': file_url, 'level':pred_count})
    return render(request, 'upload.html')