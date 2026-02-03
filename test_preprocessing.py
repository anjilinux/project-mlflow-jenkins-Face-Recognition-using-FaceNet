import numpy as np
import cv2
import pytest
from preprocessing import extract_face, get_embedding

# ---------- Fixtures ----------

@pytest.fixture
def dummy_image(tmp_path):
    """
    Create a dummy RGB image and save it temporarily
    """
    img = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
    img_path = tmp_path / "test.jpg"
    cv2.imwrite(str(img_path), img)
    return str(img_path)

# ---------- Tests ----------

def test_extract_face_shape(dummy_image):
    face = extract_face(dummy_image)
    assert face.shape == (160, 160, 3), "Face shape must be (160,160,3)"

def test_extract_face_type(dummy_image):
    face = extract_face(dummy_image)
    assert isinstance(face, np.ndarray), "Output must be numpy array"

def test_embedding_dimension(dummy_image):
    face = extract_face(dummy_image)
    embedding = get_embedding(face)

    # FaceNet default embedding size (keras-facenet)
    assert embedding.shape[0] in [128, 512], "Invalid embedding size"

def test_embedding_type(dummy_image):
    face = extract_face(dummy_image)
    embedding = get_embedding(face)
    assert isinstance(embedding, np.ndarray)

def test_embedding_not_nan(dummy_image):
    face = extract_face(dummy_image)
    embedding = get_embedding(face)
    assert not np.isnan(embedding).any(), "Embedding contains NaN values"

def test_invalid_image_path():
    with pytest.raises(Exception):
        extract_face("non_existent.jpg")
