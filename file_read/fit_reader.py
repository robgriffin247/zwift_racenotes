import fitdecode

def fit(file):
    with fitdecode.FitReader(file) as f:
        for frame in f:
            if frame.frame_type == fitdecode.FIT_FRAME_DATA:
                print(frame.name)