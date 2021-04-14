import multiprocessing as mp
import os
import sys
import zlib

from protobuf import heartbeat_pb2 as hb


class Pipeline:

    def __init__(self, log_type, nodes, output_folder, chunk_size=1000000, data_path="../data/"):
        self.log_type = log_type
        self.nodes = nodes
        self.chunk_size = chunk_size
        self.output_folder = output_folder
        self.data_path = data_path
        self.secondary_dir_path_template = output_folder \
                                           + ("sender-{}/" if log_type == "sent" else "receiver-{}/")
        self.ternary_dir_path_template = self.secondary_dir_path_template \
                                         + ("receiver-{}/" if log_type == "sent" else "sender-{}/")
        self.chunk_path_template = self.ternary_dir_path_template \
                                   + log_type \
                                   + "_{}_{}_{}-{}.pbf.gz"  # nodeOne, nodeTwo, start timestamp, end timestamp

    @staticmethod
    def __serialize_sent_log(data):
        # <site> <numseq> <timestamp send>
        send_log = hb.SendLog()
        for e in data:
            try:
                send_log.entries.add(
                    to=e[0], seq=e[1], t_sent=e[2]
                )
            except IndexError:
                print(f"**entry: {e} is ill-formatted, replaced with all 0", file=sys.stderr)
                send_log.entries.add(
                    to=0, seq=0, t_sent=0
                )
        return send_log.SerializeToString()

    @staticmethod
    def __serialize_recv_log(data):
        # <site> <numseq> <timestamp send> <timestamp receive> <hops>
        recv_log = hb.ReceiveLog()
        for e in data:
            try:
                recv_log.entries.add(
                    origin=e[0], seq=e[1], t_sent=e[2], t_received=e[3], hops=e[4]
                )
            except IndexError:
                print(f"**entry: {e} is ill-formatted, replaced with all 0", file=sys.stderr)
                recv_log.entries.add(
                    origin=0, seq=0, t_sent=0, t_received=0, hops=0
                )
        return recv_log.SerializeToString()

    @staticmethod
    def __compress(data):
        return zlib.compress(data)

    def __generate_chunk_path(self, data, node1, node2):
        start_timestamp = data[0][2] if self.log_type == 'sent' else data[0][3]
        end_timestamp = 0
        try:
            end_timestamp = data[-1][2] if self.log_type == 'sent' else data[-1][3]
        except IndexError:
            end_timestamp = data[-2][2] if self.log_type == 'sent' else data[-2][3]
        return self.chunk_path_template.format(
            node1,
            node2,
            node1,
            node2,
            start_timestamp,
            end_timestamp
        )

    def produce_single_chunk(self, data, node1, node2):
        chunk_path = self.__generate_chunk_path(data, node1, node2)
        print(f"\t\t| producing {chunk_path} containing {len(data)} entries...")
        if self.log_type == "sent":
            data = self.__serialize_sent_log(data)
        else:
            data = self.__serialize_recv_log(data)

        data = self.__compress(data)

        with open(chunk_path, 'wb') as f:
            f.write(data)
            print(f"\t\t{chunk_path} produced |")

    def process_node_to_node(self, filename, node1, node2):
        print(f"\t| Processing {filename}: node{node1}'s {self.log_type} log to node{node2}")
        data = []
        with open(filename, "r") as f:
            for line in f:
                try:
                    line = line.split(" ")
                    line = list(map(int, line))
                except ValueError:
                    print(f"{self.log_type}-{node1} line: {line} is ill formatted.", file=sys.stderr)
                    continue
                if line[0] == node2:
                    data.append(line)
                    if len(data) == self.chunk_size:
                        self.produce_single_chunk(data, node1, node2)
                        data = []
            if len(data) != 0:
                print(f"\t| Last Chunk containing {len(data)} entries")
                self.produce_single_chunk(data, node1, node2)
        print(f"\t{filename}: node{node1}'s {self.log_type} log to node{node2} processed |")

    def process_single_log(self, node, *args):
        print(f"| Processing node{node}'s {self.log_type} log")
        filename = self.data_path + "{}/{}{}.log".format(self.log_type, self.log_type, node)
        processes = []
        nodes = list(range(10))
        nodes.remove(node)
        processor = self.process_node_to_node
        for node2 in nodes:
            ternary_folder_path = self.ternary_dir_path_template.format(node, node2)
            os.makedirs(ternary_folder_path, exist_ok=True)
            p = mp.Process(target=processor, args=(filename, node, node2))
            processes.append(p)

        [p.start() for p in processes]
        [p.join() for p in processes]
        print(f"node{node}'s {self.log_type} log processed |")

    def process_all_log(self, multiprocessing=False):
        if multiprocessing:
            processes = []
            for node in self.nodes:
                secondary_folder_path = self.secondary_dir_path_template.format(node)
                os.makedirs(secondary_folder_path, exist_ok=True)
                p = mp.Process(target=self.process_single_log, args=(node, "placeholder"))
                processes.append(p)

            [p.start() for p in processes]
            [p.join() for p in processes]
        else:
            for node in self.nodes:
                secondary_folder_path = self.secondary_dir_path_template.format(node)
                os.makedirs(secondary_folder_path, exist_ok=True)
                self.process_single_log(node)
        print("--------DONE--------")
