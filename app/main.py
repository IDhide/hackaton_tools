from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import os
from model import ToolRecognitionModel
from database import Database

app = FastAPI()

# Initialize the PyTorch model
model = ToolRecognitionModel()
db = Database()

# Create a temporary folder for storing images
TEMP_FOLDER = "uploads/"
os.makedirs(TEMP_FOLDER, exist_ok=True)

@app.post("/tools/upload")
async def upload_tool(file: UploadFile = File(...)):
    try:
        # Save the uploaded image temporarily
        file_path = os.path.join(TEMP_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Use the model to recognize the tool
        result, confidence = model.recognize(file_path)

        # After processing, delete the file to save space
        os.remove(file_path)

        # Return recognition results
        return {"tool_name": result, "confidence": confidence}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/employee/update")
async def update_employee_status(tool_name: str, status: str):
    try:
        # Update employee status in the database based on tool recognition
        db.update_employee_status(tool_name, status)
        return {"message": f"Employee status updated for tool: {tool_name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
