#!/usr/bin/env bash

echo "Setting up project"

echo "Downloading model artifacts"
gdown https://drive.google.com/uc?id=1x-vDdDvaylNWd05EeRwlHEHunGdVMoLE -O models.zip

echo "Unzipping models"
unzip models.zip -d .
rm models.zip

echo "Setup completed!"


