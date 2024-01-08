docker run -it -p 6000:6000 dev-sys:v1.0
docker run -p 6002:6000 input-sys:v1.0
docker run -p 6003:4000 ingestion-sys:v1.0
docker run -p 6004:5000 prep-sys:v1.0
docker run -it -p 6005:6000 seg-sys:v1.0
docker run -p 6001:6000 prod-sys:v1.0
