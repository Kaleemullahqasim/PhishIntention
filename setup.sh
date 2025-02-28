#!/bin/bash

FILEDIR=$(pwd)

# Source the Conda configuration
CONDA_BASE=$(conda info --base)
source "$CONDA_BASE/etc/profile.d/conda.sh"
# Check if the environment already exists
conda info --envs | grep -w "myenv" > /dev/null

if [ $? -eq 0 ]; then
   echo "Activating Conda environment myenv"
   conda activate myenv
else
   echo "Creating and activating new Conda environment $ENV_NAME with Python 3.8"
   conda create -n myenv python=3.8
   conda activate myenv
fi

# Install pytorch, torchvision, detectron2
OS=$(uname -s)

if [[ "$OS" == "Darwin" ]]; then
  echo "Installing PyTorch and torchvision for macOS."
  pip install torch==1.9.0 torchvision==0.10.0 torchaudio==0.9.0
  python -m pip install detectron2 -f "https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/torch1.9/index.html"
else
  # Check if NVIDIA GPU is available for Linux and Windows
  if command -v nvcc &> /dev/null; then
    echo "CUDA is detected, installing GPU-supported PyTorch and torchvision."
    pip install torch==1.9.0+cu111 torchvision==0.10.0+cu111 torchaudio==0.9.0 -f "https://download.pytorch.org/whl/torch_stable.html"
    python -m pip install detectron2 -f "https://dl.fbaipublicfiles.com/detectron2/wheels/cu111/torch1.9/index.html"
  else
    echo "No CUDA detected, installing CPU-only PyTorch and torchvision."
    pip install torch==1.9.0+cpu torchvision==0.10.0+cpu torchaudio==0.9.0 -f "https://download.pytorch.org/whl/torch_stable.html"
    python -m pip install detectron2 -f "https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/torch1.9/index.html"
  fi
fi


# Install other requirements
pip install -r /kaggle/working/PhishIntention/requirements.txt

# Install PhishIntention as a package
pip install -v .
package_location=$(conda run -n "myenv" pip show /kaggle/working/phishintention | grep Location | awk '{print $2}')

if [ -z "PhishIntention" ]; then
  echo "Package PhishIntention not found in the Conda environment myenv."
  exit 1
else
  echo "Going to the directory of package PhishIntention in Conda environment myenv."
  cd "$package_location/phishintention" || exit
  pip install gdown
  gdown --id 1zw2MViLSZRemrEsn2G-UzHRTPTfZpaEd
  sudo apt-get update
  sudo apt-get install unzip
  unzip src.zip
fi

# Replace the placeholder in the YAML template
sed "s|CONDA_ENV_PATH_PLACEHOLDER|$package_location/phishintention|g" "$FILEDIR/phishintention/configs_template.yaml" > "$package_location/phishintention/configs.yaml"
cd "$FILEDIR"
