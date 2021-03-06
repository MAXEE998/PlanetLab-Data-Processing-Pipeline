import multiprocessing as mp
import os
import sys
import zlib

from protobuf import heartbeat_pb2 as hb


class Pipeline:

    def __init__(self, log_type, nodes, output_folder, chunk_size=1000000, data_path="../data/", index="seq"):
        self.log_type = log_type
        self.nodes = nodes
        self.chunk_size = chunk_size
        self.output_folder = output_folder
        self.data_path = data_path
        self.secondary_dir_path_template = output_folder \
                                           + ("sender-{nodeOne}/" if log_type == "sent" else "receiver-{nodeOne}/")
        self.ternary_dir_path_template = self.secondary_dir_path_template \
                                         + ("receiver-{nodeTwo}/" if log_type == "sent" else "sender-{nodeTwo}/")
        self.chunk_path_template = self.ternary_dir_path_template \
                                   + log_type \
                                   + "_{nodeOne}_{nodeTwo}_{start}-{end}.pbf.gz"
        self.index = index

    @staticmethod
    def __serialize_sent_log(data):
        # <site> <numseq> <timestamp send>
        send_log = hb.SendLog()
        for e in data:
            if len(e) != 3:
                print(f"**entry: {e} is ill-formatted, fill missing fields with -1", file=sys.stderr)
                while len(e) != 3:
                    e.append(-1)
            send_log.entries.add(
                to=e[0], seq=e[1], t_sent=e[2]
            )
        return send_log.SerializeToString()

    @staticmethod
    def __serialize_recv_log(data):
        # <site> <numseq> <timestamp send> <timestamp receive> <hops>
        recv_log = hb.ReceiveLog()
        for e in data:
            if len(e) != 5:
                print(f"**entry: {e} is ill-formatted, fill missing fields with with -1", file=sys.stderr)
                while len(e) != 5:
                    e.append(-1)
            recv_log.entries.add(
                origin=e[0], seq=e[1], t_sent=e[2], t_received=e[3], hops=e[4]
            )

        return recv_log.SerializeToString()

    @staticmethod
    def __compress(data):
        return zlib.compress(data)

    def __is_entry_valid(self, entry):
        valid_length = 3 if self.log_type == "sent" else 5
        if len(entry) != valid_length:
            return False
        return True

    def __generate_chunk_path(self, data, node1, node2):
        valid_start = data[0]
        valid_end = data[-1]

        for i in range(0, len(data)):
            if self.__is_entry_valid(data[i]):
                valid_start = data[i]
                break
        for i in range(-1, -len(data) - 1, -1):
            if self.__is_entry_valid(data[i]):
                valid_end = data[i]
                break

        if self.index == "timestamp":
            start_index = valid_start[2] if self.log_type == 'sent' else valid_start[3]
            end_index = valid_end[2] if self.log_type == 'sent' else valid_end[3]
        else:
            start_index = valid_start[1]
            end_index = valid_end[1]
        return self.chunk_path_template.format(nodeOne=node1, nodeTwo=node2, start=start_index, end=end_index)

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
                    print(f"**{self.log_type}-{node1} line: {line} is ill formatted.", file=sys.stderr)
                    line = ["-1" if i == '' else i for i in line]
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
            ternary_folder_path = self.ternary_dir_path_template.format(nodeOne=node, nodeTwo=node2)
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
                secondary_folder_path = self.secondary_dir_path_template.format(nodeOne=node)
                os.makedirs(secondary_folder_path, exist_ok=True)
                p = mp.Process(target=self.process_single_log, args=(node, "placeholder"))
                processes.append(p)

            [p.start() for p in processes]
            [p.join() for p in processes]
        else:
            for node in self.nodes:
                secondary_folder_path = self.secondary_dir_path_template.format(nodeOne=node)
                os.makedirs(secondary_folder_path, exist_ok=True)
                self.process_single_log(node)
        print("--------DONE--------")
