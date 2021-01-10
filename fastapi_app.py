from fastapi import FastAPI, Request
from starlette.responses import StreamingResponse
from PIL import Image
import io
import time

from camera import Camera
from commands import read_interoceptive_data, write_motor_command


app = FastAPI()
video = Camera()
video.start()


@app.post("/actions")
def action(body: dict):
    req_commands = body
    print(body) 
    motor_type = req_commands["motor_type"]
    position = req_commands["position"]
    speed = req_commands["speed"]
    write_motor_command(motor_type, position, speed)
    return "OK"


@app.get("/interoceptive")
async def get_interoceptive_data():
	sensors_data = {"interoceptive": read_interoceptive_data()}
	return sensors_data


@app.get("/vision")
async def get_vision():
	frame = video.read()
	
	start = time.time()
	# save array as PIL image
	image_pil = Image.fromarray(frame)
	print(f"save array as PIL in {time.time()-start} sec")
	
	start = time.time()
	# convert PIL to bytes file
	file_object = io.BytesIO()
	image_pil.save(file_object, 'PNG')
	file_object.seek(0)
	print(f"convert PIL to bytes in {time.time()-start} sec")
	
	return StreamingResponse(file_object, media_type="image/png")
	
	
@app.get("/")
def healthcheck():
	return "Pythia server is ready"
