import torch
from PIL import Image

from exampleCV import SimpleNet
from torchvision.transforms import transforms

network = SimpleNet()
# load the network
network.load_state_dict(torch.load("cifar10model_21.model"))
network.eval()
label_to_class = {1.0: 'face', 0.0: 'not'}

transforms = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(256),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])


def test_image():
    while True:
        try:
            filename = input('Filename: ')
            file = f'test/{filename}'
            image = transforms(Image.open(file).convert('RGB'))
            image = image.unsqueeze(0)
            output = network(image)
            if output.data.numpy()[0] > 0.69:
                print("face")
            else:
                print("not face")
        except Exception as e:
            print(e)


test_image()