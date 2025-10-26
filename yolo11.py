from ultralytics import YOLO

# Load a pre-trained YOLO model (adjust model type as needed)
model = YOLO("yolo11n.pt")  # n, s, m, l, x versions available

# Perform object detection on an image
results = model.predict(source="bus.jpg")  # Can also use video, directory, URL, etc.

# Display the results
results[0].show()  # Show the first image results


'''ubuntu 実行結果（errer）
yudai@yudai-VirtualBox:~/train_camera$ pip3 install ultralytics
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
    
    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
    sure you have python3-full installed.
    
    If you wish to install a non-Debian packaged Python application,
    it may be easiest to use pipx install xyz, which will manage a
    virtual environment for you. Make sure you have pipx installed.
    
    See /usr/share/doc/python3.12/README.venv for more information.

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.
'''
