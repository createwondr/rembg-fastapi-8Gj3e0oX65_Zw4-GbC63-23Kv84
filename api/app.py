from fastapi import FastAPI #import fastAPI
from pydantic import BaseModel #pydantic is to handle fastAPI request as JSON to object
from fastapi.middleware.cors import CORSMiddleware #handle CORS

from rembg import remove #rembg AI tool for bg removal
import base64 #for encode and decode image data
from io import BytesIO #to convert image to bytes

app = FastAPI()

# Add CORS middleware to allow your frontend to access the FastAPI app
origins = ["http://127.0.0.1:5503", "https://artistacademyphilippines.github.io"] #only allow these clients

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows these origins to make requests
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Allow only GET and POST methods
    allow_headers=["Content-Type"],  # Only allow the Content-Type header
)

# Define a Pydantic model to represent the request body
class RequestData(BaseModel): #convert JSON to object
    data_sent: str
    
@app.post('/')

async def remove_background(request_data: RequestData): #get object and pass it to these parameters 'request_data' variable

    # Decode the base64 string to image
    img_data = base64.b64decode(request_data.data_sent.split(',')[1])

    # Process the image with rembg to remove the background
    removed_background = remove(img_data, post_process_mask=True)

    # Convert the result into a binary format
    new_data = BytesIO(removed_background)
    new_data.seek(0)

    # Convert binary to base64 format and decode again to text format
    new_base64 = base64.b64encode(new_data.getvalue()).decode('utf-8')

    # Return the base64 string directly as HTML response (image data)
    data_received = f"data:image/png;base64,{new_base64}"
    
    return {"data_received": data_received}
