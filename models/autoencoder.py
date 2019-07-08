import tensorflow as tf
import keras
from keras.models import Model, Sequential
import keras.layers as L
import keras.backend as K
import numpy as np

def create_conv_block(model, size, init=False, input_shape=None):
    if init:
        model.add(L.Conv2D(size, (2, 2), strides=1, padding='same', activation='relu', input_shape=input_shape))
    else:
        model.add(L.Conv2D(size, (2, 2), strides=1, padding='same', activation='relu'))
    model.add(L.MaxPooling2D((2,2)))
    return model

def create_deconv_block(model, size, last=False):
    if last:
        model.add(L.Conv2D(size, (2, 2), strides=1, padding='same', activation='sigmoid'))
    else:
        model.add(L.Conv2D(size, (2, 2), strides=1, padding='same', activation='relu'))
    model.add(L.UpSampling2D((2, 2)))
    return model

def AutoEncoder_256(input_shape = (256,256,3)):
    encoder = Sequential()
    encoder.add(L.Conv2D(64, (3, 3), strides=2, padding='same', input_shape=input_shape))
    encoder.add(L.Activation('relu'))
    encoder.add(L.MaxPooling2D((2,2)))
    encoder.add(L.Conv2D(128, (3, 3), strides=2, padding='same'))
    encoder.add(L.Activation('relu'))
    encoder.add(L.MaxPooling2D((2,2)))
    encoder.add(L.Conv2D(256, (3, 3), strides=2, padding='same'))
    encoder.add(L.Activation('relu'))
    encoder.add(L.MaxPooling2D((2,2)))
    encoder.add(L.Conv2D(512, (3, 3), strides=2, padding='same'))
    encoder.add(L.Activation('relu'))
    encoder.add(L.MaxPooling2D((2,2)))
    encoder.add(L.Conv2D(1024, (3, 3), strides=2, padding='same'))
    encoder.add(L.Activation('relu', name='unflattened'))
    encoder.add(L.Flatten(name='flattened'))

    unflattened_shape = encoder.get_layer('unflattened').output_shape[1:]
    flattened_shape = encoder.get_layer('flattened').output_shape[1:]

    decoder = Sequential()
    decoder.add(L.Reshape(target_shape=unflattened_shape, input_shape=flattened_shape))
    decoder.add(L.Conv2DTranspose(512, (2, 2), strides=2, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2D(512, (3, 3), strides=1, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2DTranspose(256, (2, 2), strides=2, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2D(256, (3, 3), strides=1, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2DTranspose(128, (2, 2), strides=2, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2D(128, (3, 3), strides=1, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2DTranspose(64, (2, 2), strides=2, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2D(64, (3, 3), strides=1, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2DTranspose(32, (2, 2), strides=2, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2D(32, (3, 3), strides=1, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2DTranspose(16, (2, 2), strides=2, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2D(16, (3, 3), strides=1, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2DTranspose(8, (2, 2), strides=2, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2D(8, (3, 3), strides=1, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2DTranspose(4, (2, 2), strides=1, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2D(4, (3, 3), strides=1, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2DTranspose(3, (2, 2), strides=2, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2D(3, (3, 3), strides=1, padding='same'))
    decoder.add(L.Activation('sigmoid'))

    autoencoder = Sequential()
    autoencoder.add(encoder)
    autoencoder.add(decoder)
    return autoencoder


def AutoEncoder_128(input_shape = (128, 128, 3)):
    encoder = Sequential()
    encoder = create_conv_block(encoder, 256, init=True, input_shape=input_shape)
    encoder = create_conv_block(encoder, 256)
    encoder = create_conv_block(encoder, 512)
    encoder = create_conv_block(encoder, 512)
    encoder = create_conv_block(encoder, 1024)
    encoder = create_conv_block(encoder, 1024)
    encoder.add(L.Flatten())

    unflattened_shape = encoder.get_layer(index=-2).output_shape[1:]
    flattened_shape = encoder.get_layer(index=-1).output_shape[1:]

    decoder = Sequential()
    decoder.add(L.Reshape(target_shape=unflattened_shape, input_shape=flattened_shape))
    decoder = create_deconv_block(decoder, 1024)
    decoder = create_deconv_block(decoder, 512)
    decoder = create_deconv_block(decoder, 512)
    decoder = create_deconv_block(decoder, 256)
    decoder = create_deconv_block(decoder, 256)
    decoder = create_deconv_block(decoder, 3, last=True)

    autoencoder = Sequential()
    autoencoder.add(encoder)
    autoencoder.add(decoder)
    return autoencoder

a = AutoEncoder_128()
print(a.summary())

def AutoEncoder_64(input_shape = (64, 64, 3)):
    encoder = Sequential()
    encoder.add(L.Conv2D(64, (3, 3), strides=2, padding='same', input_shape=input_shape))
    encoder.add(L.Activation('relu'))
    encoder.add(L.MaxPooling2D((2,2)))
    encoder.add(L.Conv2D(128, (3, 3), strides=2, padding='same'))
    encoder.add(L.Activation('relu'))
    encoder.add(L.MaxPooling2D((2,2)))
    encoder.add(L.Conv2D(256, (3, 3), strides=2, padding='same'))
    encoder.add(L.Activation('relu'))
    encoder.add(L.MaxPooling2D((2,2)))
    encoder.add(L.Conv2D(512, (3, 3), strides=2, padding='same'))
    encoder.add(L.Activation('relu', name='unflattened'))
    encoder.add(L.Flatten(name='flattened'))

    unflattened_shape = encoder.get_layer('unflattened').output_shape[1:]
    flattened_shape = encoder.get_layer('flattened').output_shape[1:]

    decoder = Sequential()
    decoder.add(L.Reshape(target_shape=unflattened_shape, input_shape=flattened_shape))
    decoder.add(L.Conv2DTranspose(512, (2, 2), strides=2, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2D(512, (2, 2), strides=1, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2DTranspose(256, (2, 2), strides=2, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2D(256, (2, 2), strides=1, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2DTranspose(128, (2, 2), strides=2, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2D(128, (2, 2), strides=1, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2DTranspose(64, (2, 2), strides=2, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2D(64, (2, 2), strides=1, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2DTranspose(32, (2, 2), strides=2, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2D(32, (2, 2), strides=1, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2DTranspose(3, (2, 2), strides=2, padding='same'))
    decoder.add(L.Activation('relu'))
    decoder.add(L.Conv2D(3, (2, 2), strides=1, padding='same'))
    decoder.add(L.Activation('sigmoid'))

    autoencoder = Sequential()
    autoencoder.add(encoder)
    autoencoder.add(decoder)
    return autoencoder

def VAE(optimizer, latent_dim=512):
    encoder_input = L.Input(shape=(256, 256, 3), name='encoder_input')
    en = L.Conv2D(64, (3, 3), padding='same')(encoder_input)
    en = L.BatchNormalization()(en)
    en = L.Activation('relu')(en)
    en = L.MaxPooling2D((2, 2))(en)
    en = L.Conv2D(64, (3, 3), padding='same')(en)
    en = L.BatchNormalization()(en)
    en = L.Activation('relu')(en)
    en = L.MaxPooling2D((2, 2))(en)
    en = L.Conv2D(128, (3, 3), padding='same')(en)
    en = L.BatchNormalization()(en)
    en = L.Activation('relu')(en)
    en = L.MaxPooling2D((2, 2))(en)
    en = L.Conv2D(128, (3, 3), padding='same')(en)
    en = L.BatchNormalization()(en)
    en = L.Activation('relu')(en)
    en = L.MaxPooling2D((2, 2))(en)
    en = L.Conv2D(256, (3, 3), padding='same')(en)
    en = L.BatchNormalization()(en)
    en = L.Activation('relu')(en)
    en = L.MaxPooling2D((2, 2))(en)
    en = L.Conv2D(512, (3, 3), padding='same')(en)
    en = L.BatchNormalization()(en)
    en = L.Activation('relu')(en)
    en = L.MaxPooling2D((2, 2))(en)
    en = L.Conv2D(512, (3, 3), padding='same')(en)
    en = L.BatchNormalization()(en)
    en = L.Activation('relu')(en)
    en = L.MaxPooling2D((2, 2))(en)

    unflatted_shape = K.int_shape(en)
    flatted= L.Flatten(name='encoder_output')(en)

    z_mean = L.Dense(latent_dim, name='z_mean')(flatted)
    z_log_var = L.Dense(latent_dim, name='z_log_var')(flatted)
    z = L.Lambda(_sampling, output_shape=(latent_dim,), name='z')([z_mean, z_log_var])

    decoder_input = L.Input(shape=(latent_dim, ), name='decoder_input')
    de = L.Dense(np.prod(unflatted_shape[1:]))(decoder_input)
    de = L.Reshape((unflatted_shape[1:]))(de)
    de = L.Conv2DTranspose(512, (2, 2), strides=2, padding='same')(de)
    de = L.Conv2D(512, (3, 3), padding='same')(de)
    de = L.BatchNormalization()(de)
    de = L.Activation('relu')(de)
    de = L.Conv2DTranspose(512, (2, 2), strides=2, padding='same')(de)
    de = L.Conv2D(512, (3, 3), padding='same')(de)
    de = L.BatchNormalization()(de)
    de = L.Activation('relu')(de)
    de = L.Conv2DTranspose(256, (2, 2), strides=2, padding='same')(de)
    de = L.Conv2D(256, (3, 3), padding='same')(de)
    de = L.BatchNormalization()(de)
    de = L.Activation('relu')(de)
    de = L.Conv2DTranspose(128, (2, 2), strides=2, padding='same')(de)
    de = L.Conv2D(128, (3, 3), padding='same')(de)
    de = L.BatchNormalization()(de)
    de = L.Activation('relu')(de)
    de = L.Conv2DTranspose(128, (2, 2), strides=2, padding='same')(de)
    de = L.Conv2D(128, (3, 3), padding='same')(de)
    de = L.BatchNormalization()(de)
    de = L.Activation('relu')(de)
    de = L.Conv2DTranspose(64, (2, 2), strides=2, padding='same')(de)
    de = L.Conv2D(64, (3, 3), padding='same')(de)
    de = L.BatchNormalization()(de)
    de = L.Activation('relu')(de)
    de = L.Conv2DTranspose(3, (2, 2), strides=2, padding='same')(de)
    de = L.Conv2D(3, (3, 3), padding='same')(de)
    decoded = L.Activation('sigmoid')(de)

    encoder = Model(encoder_input, [z_mean, z_log_var, z], name='encoder')
    decoder = Model(decoder_input, decoded, name='decoder')
    output = decoder(encoder(encoder_input)[2])

    def vae_loss(y_true, y_pred, z_mean=z_mean, z_log_var=z_log_var):
        reconstruction_loss = (256*256) * K.mean(keras.losses.mse(y_true, y_pred), axis=[1,2])
        kl_loss = -0.5 * K.sum(1 + z_log_var - K.square(z_mean) - K.exp(z_log_var), axis=1)
        vae_loss = K.mean(reconstruction_loss + kl_loss)
        return vae_loss

    vae = Model(encoder_input, output)
    vae.compile(
        optimizer=optimizer,
        loss=vae_loss)

    return vae

def _sampling(args):
    z_mean, z_log_var = args
    batch = K.shape(z_mean)[0]
    dim = K.int_shape(z_mean)[1]
    epsilon = K.random_normal(shape=(batch, dim))
    return z_mean + K.exp(0.5 * z_log_var) * epsilon
