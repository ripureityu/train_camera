# このスクリプトの目的:
# - 内蔵カメラでリアルタイムにフレームを取得する
# - 取得したフレームを YOLO(yolo11n.pt) で解析して物体検出を行う
# - 物体が検知されたら検出ボックス付きの画像を画面に表示する
# - 物体が検知されなかったら画面上に「No object detected」のメッセージを表示する
# - 'q' キーで終了する
import time
import cv2
import numpy as np
from ultralytics.models.yolo import YOLO

model = YOLO("yolo11n.pt")


def find_camera_index(max_index=4, wait=0.2):
    for i in range(max_index):
        cap = cv2.VideoCapture(i)
        time.sleep(wait)
        if not cap or not cap.isOpened():
            try:
                cap.release()
            except Exception:
                pass
            continue
        ret, _ = cap.read()
        cap.release()
        if ret:
            return i
    return -1


def _cls_tensor_to_list(cls_obj):
    try:
        if hasattr(cls_obj, "cpu") and hasattr(cls_obj, "numpy"):
            return cls_obj.cpu().numpy().astype(int).tolist()
    except Exception:
        pass
    try:
        import numpy as _np
        if isinstance(cls_obj, _np.ndarray):
            return cls_obj.astype(int).tolist()
    except Exception:
        pass
    try:
        if isinstance(cls_obj, list):
            return [int(x) for x in cls_obj]
    except Exception:
        pass
    return []


def detect_any_object_from_result(r):
    try:
        boxes = getattr(r, "boxes", None)
        if boxes is None:
            return False
        data = getattr(boxes, "data", None)
        if data is not None:
            try:
                arr = data.cpu().numpy() if hasattr(data, "cpu") else np.array(data)
                if arr.shape[0] > 0:
                    return True
            except Exception:
                pass
        cls_obj = getattr(boxes, "cls", None)
        cls_list = _cls_tensor_to_list(cls_obj) if cls_obj is not None else []
        if len(cls_list) > 0:
            return True
    except Exception:
        pass
    try:
        if hasattr(r, "summary"):
            for item in (r.summary() or []):
                if item.get("name") is not None:
                    return True
    except Exception:
        pass
    return False


def main():
    cam_idx = find_camera_index(max_index=6)
    if cam_idx < 0:
        print("ERROR: カメラが見つかりません。/dev/video* を確認してください。")
        return

    cap = cv2.VideoCapture(cam_idx)
    if not cap.isOpened():
        print(f"ERROR: カメラ index {cam_idx} を開けませんでした。")
        return

    print(f"Using camera index {cam_idx}. Press 'q' to quit.")
    window_shown = False
    while True:
        ret, frame = cap.read()
        if not ret:
            print("フレーム取得失敗。終了します。")
            break

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        try:
            results = model.predict(source=[img_rgb], imgsz=640, conf=0.25, verbose=False)
        except Exception as e:
            print("model.predict エラー:", e)
            results = None

        detected = False
        annotated = None
        if results and len(results) > 0:
            r = results[0]
            detected = detect_any_object_from_result(r)
            try:
                annotated = r.plot()
            except Exception:
                annotated = None

        if detected:
            # 物体検知がある場合のみ表示
            if annotated is not None:
                try:
                    if annotated.ndim == 3 and annotated.shape[2] == 3:
                        annotated_bgr = cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR)
                    else:
                        annotated_bgr = annotated
                except Exception:
                    annotated_bgr = annotated
                cv2.imshow("YOLO Detection", annotated_bgr)
            else:
                # アノテーションが取得できない場合は元フレームを表示
                cv2.imshow("YOLO Detection", frame)
            window_shown = True
        else:
            # 物体検知なし: 表示ウィンドウが開いていれば閉じる。画面には何も出力しない。
            if window_shown:
                try:
                    cv2.destroyWindow("YOLO Detection")
                except Exception:
                    pass
                window_shown = False

        # 'q' で終了（ウィンドウが無いとキー検出できない場合がある）
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    try:
        cv2.destroyAllWindows()
    except Exception:
        pass


if __name__ == "__main__":
    main()




