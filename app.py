import os
import zipfile

import fitz  # PyMuPDF 库用于处理 PDF 文件
from flask import Flask, request, render_template, jsonify, send_file

app = Flask(__name__)

# 定义上传和输出文件的目录
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ZIP_FOLDER = 'zips'

# 创建目录如果它们不存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(ZIP_FOLDER, exist_ok=True)

@app.route('/')
def index():
    # 主页路由，返回 HTML 模板
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "没有文件上传"}), 400

    file = request.files['file']
    if file and file.filename.endswith('.pdf'):
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        images = extract_images(filepath)

        if not images:
            return jsonify({"error": "未能转换任何图像"}), 400

        zip_filename = create_zip(images, filename)
        if not zip_filename:
            return jsonify({"error": "生成ZIP文件失败"}), 500

        response = {
            "message": "文件转换成功",
            "images": [f'/output/{img}' for img in images],
            "zip_file": f'/zips/{zip_filename}'
        }
        return jsonify(response), 200
    else:
        return jsonify({"error": "文件类型不支持"}), 400

def extract_images(pdf_path):
    # 提取 PDF 中的图像并保存
    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))
        output_filename = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_{page_num + 1}.png"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        pix.save(output_path)
        images.append(output_filename)
    return images

def create_zip(images, base_name):
    # 将提取的图像打包成 ZIP 文件
    zip_filename = f"{os.path.splitext(base_name)[0]}.zip"
    zip_filepath = os.path.join(ZIP_FOLDER, zip_filename)
    try:
        with zipfile.ZipFile(zip_filepath, 'w') as zipf:
            for image in images:
                zipf.write(os.path.join(OUTPUT_FOLDER, image), image)
        return zip_filename
    except Exception as e:
        print(f"生成ZIP文件失败: {e}")
        return None

@app.route('/zips/<filename>')
def download_zip(filename):
    # 提供 ZIP 文件下载的路由
    zip_path = os.path.join(ZIP_FOLDER, filename)
    return send_file(zip_path, as_attachment=True)

@app.route('/output/<filename>')
def send_image(filename):
    # 提供转换后图像的路由
    return send_file(os.path.join(OUTPUT_FOLDER, filename))

if __name__ == '__main__':
    app.run(debug=True)
# app.run(host='0.0.0.0', port=5000, debug=True)   这行代码用于部署服务器，允许外部访问
