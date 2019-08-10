import argparse
import keras
import keras.layers as L
import keras.backend as K


import utils
from utils.models import ConvLSTM
from utils.data import Dataset

# argparse
parser = argparse.ArgumentParser()
parser.add_argument('--train', type=str, default='train')
parser.add_argument('--directory', type=str)
parser.add_argument('--save_path', type=str)
parser.add_argument('--epochs', type=int, default=100)
parser.add_argument('--steps_per_epoch', type=int, default=100)
parser.add_argument('--batch_size', type=int, default=32)
parser.add_argument('--batch_per_video', type=int, default=4)
parser.add_argument('--offset_x', nargs='+', type=int, default=[1, 7, 15])
parser.add_argument('--offset_y', type=int, default=30)

args = parser.parse_args()


def train(dataloader, model, epochs, steps_per_epoch):
    hist = model.fit_generator(
        generator=dataloader,
        epochs = epochs,
        steps_per_epoch= steps_per_epoch
    )
    return

def test():
    return

def main(args):
    dataset = Dataset(args.directory, args.offset_x, args.offset_y, args.batch_size, args.batch_per_video)

    if args.train == 'train':
        dataloader = dataset.trainloader()
        optimizer = keras.optimizers.Adam(lr=1e-3, decay=1e-4)
        model = ConvLSTM(optimizer=optimizer)
        train(dataloader, model, args.epochs, args.steps_per_epoch)
        utils.save_model(model, args.save_path)

    else:
        dataloader = dataset.testloader()
        model = utils.load_model(save_path)
        test()

if __name__ == '__main__':
    main(args)
