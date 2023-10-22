from PIL import Image
from torch.autograd import Variable
from torchvision.transforms import ToTensor, ToPILImage
from model import Generator
import torch


def apply_srgan(image_path, output_path,super_size):

    TEST_MODE = False  # 默认使用CPU，如果需要使用GPU，请将其设置为True
    if super_size==2:
        UPSCALE_FACTOR = 2
        MODEL_NAME = 'netG_epoch_2_100.pth'
    elif super_size==4:
        UPSCALE_FACTOR = 4
        MODEL_NAME = 'netG_epoch_4_100.pth'
    elif super_size==8:
        UPSCALE_FACTOR = 8
        MODEL_NAME = 'netG_epoch_8_100.pth'

    model = Generator(UPSCALE_FACTOR).eval()

    if TEST_MODE:
        model.cuda()
        model.load_state_dict(torch.load('model/' + MODEL_NAME))
    else:
        model.load_state_dict(torch.load('model/' + MODEL_NAME, map_location=lambda storage, loc: storage))

    image = Image.open(image_path)
    image = Variable(ToTensor()(image)).unsqueeze(0)

    if TEST_MODE:
        image = image.cuda()

    with torch.no_grad():
        out = model(image)

    out_img = ToPILImage()(out[0].data.cpu())
    out_img.save(output_path)

# apply_srgan("test_images/baboon.png", "output_images/out_baboon.png")