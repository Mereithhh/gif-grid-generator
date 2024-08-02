# 使用官方的 Python 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 将 requirements.txt 文件复制到容器中
COPY requirements.txt .

# 安装 Python 依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 将当前目录下的所有文件复制到工作目录中
COPY . .

# 公开端口 8881
EXPOSE 8881

# 设置环境变量以确保 Python 输出直接转到终端而不是缓冲区
ENV PYTHONUNBUFFERED=1

# 运行 Flask 应用
CMD ["python", "app.py"]
