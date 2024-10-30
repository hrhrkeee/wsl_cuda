# WSL-CUDA

WSL2上でGPU利用可能なDockerコンテナを手軽に作成できるように

## 利用方法

GPUドライバは事前にインストールする

利用したい環境のフォルダへ移動して`docker compose up -d`で起動する

VSCodeの拡張機能でコンテナにアタッチする

## ベースコンテナの探し方

下記ページから探す  
[https://hub.docker.com/r/nvidia/cuda](https://hub.docker.com/r/nvidia/cuda)