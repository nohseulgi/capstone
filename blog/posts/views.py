from crowdnet.datautils import load_image, resize_img, preprocess_transform, count_from_density_map
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
# Create your views here.
from crowdnet.train import LitCrowdNet
import torch
import argparse
from pathlib import Path


def get_args():
    parser = argparse.ArgumentParser()

    model_group = parser.add_mutually_exclusive_group(required=True)
    model_group.add_argument("--ckpt-path", type=str, default="", help="Checkpoint path.")
    model_group.add_argument("--model-path", type=str, default="./model/model.pt", help="Saved model path.")
    parser.add_argument("--device", type=str, default="cpu", help="Device to load model on.")
    parser.add_argument("--img-path", type=Path, default="./blog/media/000.jpg", help="Image path.", required=True)
    parser.add_argument("--dataset-root", type=Path, help="Path to JHU Crowd++ dataset.")
    parser.add_argument("--subset", type=str, default="test", help="Subset.")
    return parser.parse_args()


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

        args = get_args()
        #       def get_args():
        #          parser = argparse.ArgumentParser()
        #
        #          model_group = parser.add_mutually_exclusive_group(required=True)
        #         model_group.add_argument("--ckpt-path", type=str, default="", help="Checkpoint path.")
        #           model_group.add_argument("--model-path", type=str, default="./model/model.pt", help="Saved model path.")
        #          parser.add_argument("--device", type=str, default="cpu", help="Device to load model on.")
        #          parser.add_argument("--img-path", type=Path, help="Image path.", required=True)
        #          parser.add_argument("--dataset-root", type=Path, help="Path to JHU Crowd++ dataset.")
        #          parser.add_argument("--subset", type=str, default="test", help="Subset.")

        #          return parser.parse_args()

        if args.ckpt_path:
            model = LitCrowdNet.load_from_checkpoint(args.ckpt_path, map_location=args.device)
            model.eval()
        else:
            model = torch.load(args.model_path, map_location=args.device)
            model.eval()

        img = load_image(args.img_path)
        img, resize_ratio = resize_img(img)

        img_input = preprocess_transform(img).unsqueeze(dim=0)
        pred_density_map = model(img_input).detach().cpu().numpy()[0][0]

        pred_count = count_from_density_map(pred_density_map)

        return render(request, 'upload.html', {'file_url': file_url, 'level': pred_count})
    return render(request, 'upload.html')
