# 使用官方 Ubuntu 镜像作为基础镜像
FROM ubuntu:latest


ARG OPENAI_API_KEY
# 设置工作目录
WORKDIR /easytool

# 将当前目录下的所有文件复制到容器中
COPY . .

# 安装必要的软件包和依赖项
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-venv python3-pip \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /root/.cache \
    && python3 -m venv /venv \
    && /venv/bin/pip install google-search-results numexpr \
    && /venv/bin/pip install -r requirements.txt \
    && sed -i "s/^OPENAI_API_KEY=.*/OPENAI_API_KEY=${OPENAI_API_KEY}/" .env
#创建用户用户组
RUN groupadd -g 1001 easytool \
    && useradd -u 1001 -g easytool -s /bin/bash -m easytool
# 暴露端口
EXPOSE 13001

USER easytool

# 启动应用程序
CMD ["/venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "13001"]

