from PIL import Image, ImageOps

def create_mirrored_gif(input_path, output_path):
    # 打开原始 GIF
    original_gif = Image.open(input_path)

    # 获取所有帧
    frames = []
    try:
        while True:
            frame = original_gif.copy()
            mirrored_frame = ImageOps.mirror(frame)
            frames.append((frame, mirrored_frame))
            original_gif.seek(len(frames))  # 移动到下一帧
    except EOFError:
        pass  # 已经处理完所有帧

    # 创建新的帧列表
    new_frames = []
    for frame, mirrored_frame in frames:
        top_row = Image.new("RGBA", (frame.width * 2, frame.height))
        bottom_row = Image.new("RGBA", (frame.width * 2, frame.height))
        
        top_row.paste(frame, (0, 0))
        top_row.paste(mirrored_frame, (frame.width, 0))
        
        bottom_row.paste(frame, (0, 0))
        bottom_row.paste(mirrored_frame, (frame.width, 0))
        
        new_frame = Image.new("RGBA", (frame.width * 2, frame.height * 2))
        new_frame.paste(top_row, (0, 0))
        new_frame.paste(bottom_row, (0, frame.height))
        
        new_frames.append(new_frame)

    # 保存新的 GIF
    new_frames[0].save(output_path, save_all=True, append_images=new_frames[1:], loop=0, duration=original_gif.info['duration'])

# 使用示例
input_path = 'input.gif'
output_path = 'output.gif'
create_mirrored_gif(input_path, output_path)
