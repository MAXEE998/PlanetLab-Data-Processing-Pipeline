import pathlib
import sys
import zlib

from protobuf import heartbeat_pb2 as hb


def decode(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    data = zlib.decompress(data)

    if log_type == "sent":
        pbf = hb.SendLog()
    else:
        pbf = hb.ReceiveLog()

    pbf.ParseFromString(data)
    return pbf


if __name__ == "__main__":
    path = sys.argv[1].replace(pathlib.os.sep, "/")
    log_type = path.split("/")[-1].split("_")[0]
    d = decode(path)
    print(d.entries)
