docker build -t mkdocs:latest .
docker run -d -p 8000:8000 -v $(pwd):/docs mkdocs:latest