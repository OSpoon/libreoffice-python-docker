FROM python:3.11-slim

LABEL maintainer="OSpoon <zxin088@gmail.com>" \
    description="Python with LibreOffice base image for document processing" \
    version="24.8.6"

WORKDIR /app

# 配置apt源为阿里云镜像
RUN echo \
    "deb https://mirrors.aliyun.com/debian/ bookworm main contrib non-free non-free-firmware\n\
    deb https://mirrors.aliyun.com/debian/ bookworm-updates main contrib non-free non-free-firmware\n\
    deb https://mirrors.aliyun.com/debian-security bookworm-security main contrib non-free non-free-firmware" \
    > /etc/apt/sources.list

# 安装基础工具和Python环境
RUN apt-get update && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get install -y \
    # 基础构建工具
    wget \
    # 添加 Java 运行环境
    default-jre \
    # 必要依赖
    libxslt1.1 \
    # 字体支持
    fonts-noto-cjk \
    fonts-noto-color-emoji

# 下载并安装 LibreOffice
RUN cd /tmp && \
    wget -O LibreOffice.tar.gz https://mirrors.cloud.tencent.com/libreoffice/libreoffice/stable/24.8.6/deb/x86_64/LibreOffice_24.8.6_Linux_x86-64_deb.tar.gz && \
    tar xzf LibreOffice.tar.gz && \
    cd LibreOffice_24.8.6*/DEBS/ && \
    dpkg -i *.deb && \
    # 创建符号链接到标准目录
    ln -sf /opt/libreoffice24.8/program/soffice /usr/bin/libreoffice && \
    # 清理下载文件
    cd /tmp && \
    rm -rf LibreOffice* && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 配置环境变量
ENV LIBREOFFICE_PATH=/usr/bin/libreoffice \
    PYTHONHOME=/usr/local \
    PYTHONPATH=/usr/local/lib/python3.11:/usr/local/lib/python3.11/lib-dynload:/usr/local/lib/python3.11/site-packages

RUN mkdir -p /app/input /app/output

COPY convert.py /app/
