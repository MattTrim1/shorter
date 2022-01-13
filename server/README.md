# Server

This is the API server for `shorter`.

## How to use
The API is written with a Dockerfile, so should be launched as follows:
```bash
docker build -t shorter-api:latest -f Dockerfile .
docker run -p 5000:5000 shorter-api:latest
```
