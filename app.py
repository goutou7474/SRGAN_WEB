from flask import Flask, request, jsonify, send_file, render_template
import os
import uuid   # <-- 导入 uuid 库
from test_image import apply_srgan

app = Flask(__name__)

# 设置上传文件夹路径
UPLOAD_FOLDER = 'test_images'
OUTPUT_FOLDER= 'static/output_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
# 定义允许上传的文件扩展名
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    super_size = request.form.get('scale')
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        # 生成唯一文件名
        unique_filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()

        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)

        # 使用唯一文件名保存处理后的图片
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], 'processed_' + unique_filename)
        apply_srgan(file_path, output_path, int(super_size))

        # 返回处理后的图片文件名和URL路径
        return jsonify({'filename': 'processed_' + unique_filename, 'url': os.path.join(app.config['OUTPUT_FOLDER'], 'processed_' + unique_filename)})
    return jsonify({'error': 'File format not supported'})

if __name__ == '__main__':
    app.run(debug=True)
