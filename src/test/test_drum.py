from src.song import drum


def test_load_scaler():
    assert drum.scale_features([1]*26).all()
