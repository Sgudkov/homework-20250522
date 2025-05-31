"""
FastAPI Application
====================
"""

import soundfile as sf
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from kokoro import KPipeline
from pydantic import BaseModel

"""
Application Configuration
-------------------------

* `pipeline`: KPipeline instance for text-to-speech conversion
* `app`: FastAPI application instance
"""

pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")

app = FastAPI()

"""
User Information Model
----------------------

* `Text`: str - user input text
"""


class UserInfo(BaseModel):
    Text: str


"""
Root Endpoint
-------------

* **POST /**: accepts user input text and returns a streaming audio response
* **Request Body**: [UserInfo](#user-information-model) model
* **Response**: `StreamingResponse` with audio data
"""


@app.post("/")
async def root(user_info: UserInfo):
    """
    Handles user input text and generates audio response using KPipeline.

    :param user_info: UserInfo model containing user input text
    :return: StreamingResponse with audio data
    """
    text = user_info.Text

    if text is None:
        text = "This is a sample text."

    generator = pipeline(text, voice="af_heart")

    def audio_file_generator(file_path: str):
        """
        Generator function for streaming audio data.

        :param file_path: str - path to audio file
        :yield: bytes - audio data chunks
        """
        with open(file_path, "rb") as f:
            while chunk := f.read(1024):  # Read in 1KB chunks
                yield chunk

    for i, (gs, ps, audio) in enumerate(generator):
        sf.write(f"{i}.wav", audio, 24000)
        return StreamingResponse(
            audio_file_generator(f"{i}.wav"), media_type="audio/wav"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8005, reload=True)
