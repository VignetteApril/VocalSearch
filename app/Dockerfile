# 使用官方 Python 基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制应用代码和依赖文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install modelscope
RUN pip install python-docx
RUN pip install fpdf

# 安装系统依赖，包括中文字体
RUN apt-get update && apt-get install -y \
    ffmpeg \
    fonts-noto-cjk

# 安装 fontforge 和其他字体工具
RUN apt-get install -y \
    fontforge \
    ttf-wqy-zenhei \
    ttf-wqy-microhei

# 将 NotoSansCJK-Regular.ttc 转换为 TTF
RUN mkdir -p /usr/share/fonts/ttf/noto && \
    fontforge -lang=ff -c 'Open("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"); Generate("/usr/share/fonts/ttf/noto/NotoSansCJK-Regular.ttf");'

# 更新字体缓存
RUN fc-cache -fv

RUN pip install gradio_pdf
RUN pip install docx2pdf
RUN pip install Spire.Doc
RUN pip install reportlab

# 复制项目文件
COPY . .

# 暴露应用的默认端口
EXPOSE 7860

# 启动应用
CMD ["python", "main.py"]
