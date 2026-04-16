#!/usr/bin/env bash

echo "Setting up project"

echo "Downloading model artifacts"
gdown https://drive.google.com/uc?id=1pjk69tDNgDaj4Z2y-ZBK8rkly8m_2uwm -O models.zip

echo "Unzipping models"
unzip models.zip -d .
rm models.zip

echo "Setup completed!"


