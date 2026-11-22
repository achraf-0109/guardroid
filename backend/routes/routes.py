from pathlib import Path
from tempfile import TemporaryDirectory
from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from config import ALLOWED_EXTENSIONS, MAX_UPLOAD_SIZE
from services.predictor import predict_apk

router = APIRouter()

@router.get("/")
def health():
    return {"status": "ready"}

@router.post("/predict")
def predict(request: Request, file: UploadFile = File(...)):
    extension = Path(file.filename or "").suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Please upload an APK file.",
        )

    try:
        with TemporaryDirectory() as temp_dir:
            apk_path = Path(temp_dir) / "upload.apk"
            size = 0

            with apk_path.open("wb") as destination:
                while chunk := file.file.read(1024 * 1024):
                    size += len(chunk)

                    if size > MAX_UPLOAD_SIZE:
                        raise HTTPException(
                            status_code=413,
                            detail="APK exceeds the upload size limit.",
                        )

                    destination.write(chunk)

            if size == 0:
                raise HTTPException(
                    status_code=400,
                    detail="The uploaded file is empty.",
                )
            return predict_apk(
                apk_path=apk_path,
                model=request.app.state.model,
                feature_names=request.app.state.features,
            )
    finally:
        file.file.close()