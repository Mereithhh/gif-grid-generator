import base64
import io
from flask import Flask, request, jsonify, render_template
from PIL import Image, ImageOps

app = Flask(__name__)

def process_gif(data, config):
    # 解码 base64 数据
    gif_data = base64.b64decode(data)
    original_gif = Image.open(io.BytesIO(gif_data))
    
    # 获取所有帧
    frames = []
    try:
        while True:
            frame = original_gif.copy()
            frames.append(frame)
            original_gif.seek(len(frames))  # 移动到下一帧
    except EOFError:
        pass  # 已经处理完所有帧
    
    # 处理每一帧
    new_frames = []
    for frame in frames:
        # 创建一个新的 NxN 帧
        width, height = frame.width, frame.height
        n = len(config['pos'])
        new_frame = Image.new("RGBA", (width * n, height * n))
        
        for i, row in enumerate(config['pos']):
            for j, val in enumerate(row):
                temp_frame = frame.copy()
                if val == 1:
                    temp_frame = ImageOps.mirror(temp_frame)
                elif val == 90:
                    temp_frame = temp_frame.rotate(-90, expand=True)
                elif val == 180:
                    temp_frame = temp_frame.rotate(180, expand=True)
                elif val == 270:
                    temp_frame = temp_frame.rotate(90, expand=True)
                
                new_frame.paste(temp_frame, (j * width, i * height))
        
        new_frames.append(new_frame)
    
    # 保存新的 GIF
    output_buffer = io.BytesIO()
    new_frames[0].save(output_buffer, format='GIF', save_all=True, append_images=new_frames[1:], loop=0, duration=original_gif.info['duration'])
    
    # 编码为 base64
    output_data = base64.b64encode(output_buffer.getvalue()).decode('utf-8')
    return output_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/gif', methods=['POST'])
def gif_api():
    try:
        # 获取 JSON 数据
        req_data = request.get_json()
        gif_data = req_data.get('data')
        config = req_data.get('config')
        
        # 处理 GIF
        output_data = process_gif(gif_data, config)
        
        # 返回结果
        return jsonify({
            'success': True,
            'message': 'GIF processed successfully',
            'data': output_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e),
            'data': None
        })

if __name__ == '__main__':
    app.run(port=8881)
