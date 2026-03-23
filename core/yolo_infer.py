from ultralytics import YOLO


def infer_image(model_path, image_path, conf=0.25):
    """
    返回格式：
    [
        [cls_id, cx, cy, w, h],
        ...
    ]
    坐标均为 YOLO 归一化格式
    """
    model = YOLO(model_path)
    results = model.predict(source=image_path, conf=conf, verbose=False)

    boxes_out = []
    if not results:
        return boxes_out

    result = results[0]
    if result.boxes is None:
        return boxes_out

    xywhn = result.boxes.xywhn
    cls_ids = result.boxes.cls

    if xywhn is None or cls_ids is None:
        return boxes_out

    xywhn = xywhn.cpu().tolist()
    cls_ids = cls_ids.cpu().tolist()

    for box, cls_id in zip(xywhn, cls_ids):
        cx, cy, w, h = box
        boxes_out.append([int(cls_id), float(cx), float(cy), float(w), float(h)])

    return boxes_out
