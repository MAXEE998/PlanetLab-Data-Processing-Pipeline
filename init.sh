pip3 install -r requirements.txt

# if you have installed it before but with a different version
# pip3 install --upgrade protobuf


# install protobuf
# skip

# compile
SRC_DIR="./protobuf"
DST_DIR="./protobuf"


protoc -I=$SRC_DIR --python_out=$DST_DIR $SRC_DIR/heartbeat.proto