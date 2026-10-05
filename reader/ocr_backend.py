"""OCR backend chooser.

PaddleOCR is the primary engine. Where PaddleOCR (or its model download) is not
available, RapidOCR runs the same PP-OCR detection/recognition models through
ONNX Runtime, with the models bundled in the pip package. This adapter gives it
the same .predict() interface read_scan.py expects.
"""


class _Res:
    def __init__(self, texts, scores):
        self.json = {"res": {"rec_texts": texts, "rec_scores": scores}}


class RapidOCRAdapter:
    def __init__(self):
        from rapidocr_onnxruntime import RapidOCR
        self._ocr = RapidOCR()

    def predict(self, image_path):
        result, _ = self._ocr(str(image_path))
        result = result or []
        return [_Res([r[1] for r in result], [float(r[2]) for r in result])]


def make_engine():
    try:
        from paddleocr import PaddleOCR
        return PaddleOCR(text_detection_model_name="PP-OCRv5_mobile_det", text_recognition_model_name="PP-OCRv5_mobile_rec",
                         use_doc_orientation_classify=False, use_doc_unwarping=False, use_textline_orientation=False,
                         device="cpu", enable_mkldnn=False)
    except Exception:
        return RapidOCRAdapter()
