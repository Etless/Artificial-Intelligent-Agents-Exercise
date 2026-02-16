import os

from ultralytics import YOLO

def task3():
    # Base path to build other directories from
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Variables
    DIR_NAME = os.path.join(BASE_DIR,"data")

    model = YOLO("yolov8n-cls.pt")
    print("Model task:", model.task) # Needs to be "classify"

    train_results = model.train(
        data=str(DIR_NAME),
        imgsz=224,
        epochs=30,
        batch=32
    )

    metrics = model.val(data=DIR_NAME, plots=True)
    return metrics