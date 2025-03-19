def draw_rectangle(frame, coordinates, color=(0, 255, 0), thickness=2):
    x, y, w, h = coordinates
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)

def save_video(frames, output_file):
    if not frames:
        return
    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_file, fourcc, 20.0, (width, height))
    
    for frame in frames:
        out.write(frame)
    
    out.release()