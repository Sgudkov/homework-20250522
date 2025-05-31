# Text-to-Speech API
=====================

## Overview

This API uses a KPipeline instance to generate audio responses from user input text.

## API Endpoint

### POST /

Accepts user input text and returns a streaming audio response.

#### Request Body

* `Text`: str - user input text

#### Response

* `audio/wav` - streaming audio response

## KPipeline

The KPipeline instance used in this API is from the [Kokoro repository](https://github.com/hexgrad/kokoro). Please refer to the repository for more information on KPipeline and its usage.

## Running the API

To start the API server, run the following command:
```bash
uvicorn main:app --host 127.0.0.1 --port 8005 --reload