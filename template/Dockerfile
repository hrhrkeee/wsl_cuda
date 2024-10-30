# ベースイメージとしてnvidia/cuda:11.8.0-base-ubuntu20.04を使用
FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

# 環境変数の設定
ENV DEBIAN_FRONTEND=noninteractive

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    curl \
    ca-certificates \
    libssl-dev \
    libffi-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# VSCodeのインストール
RUN echo "code code/add-microsoft-repo boolean true" | debconf-set-selections && \
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg && \
install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg && \
echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" | tee /etc/apt/sources.list.d/vscode.list > /dev/null && \
rm -f packages.microsoft.gpg
RUN apt install -y apt-transport-https && \
    apt update && \
    apt install -y code && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Miniforge3のインストール
RUN wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh -O Miniforge3.sh \
    && bash Miniforge3.sh -b -p /opt/conda \
    && rm Miniforge3.sh

# condaのパスを通す
ENV PATH=/opt/conda/bin:$PATH

# condaを初期化
RUN /opt/conda/bin/conda init bash

# シェルを再初期化するために、`bash` を再実行
SHELL ["/bin/bash", "-c"]

# Python 3.10をインストール
RUN conda install python=3.10

# PyTorchをインストール
RUN pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 --index-url https://download.pytorch.org/whl/cu118

# OpenCVをインストール
RUN apt -y update && apt -y upgrade
RUN apt -y install libopencv-dev
RUN pip install opencv-python

# その他のライブラリをインストール
RUN pip install ultralytics ipykernel

# PythonとCUDAが正常にインストールされていることを確認するためのコマンドを実行
RUN python --version && nvcc --version


# デフォルトのシェルとしてbashを使用
CMD ["/bin/bash"]
