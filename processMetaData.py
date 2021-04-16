import json
import pathlib
import sys


class MetaDataProcessor:

    def __init__(self, path):
        self.path = path.replace(pathlib.os.sep, '/')

    @staticmethod
    def splitter(t):
        # result should look like
        # [type, node1, node2, (start_index, end_index)]
        s = t[0]
        s = s.split('.')[0]
        s = s.split('_')
        s[-1] = tuple(s[-1].split('-'))
        return s, t[1]

    @staticmethod
    def process_log_level1(raw_level1):
        processed = dict()
        # separate by node 1
        start = 0
        for i in range(len(raw_level1)):
            if i == (len(raw_level1) - 1) or raw_level1[i][0][1] != raw_level1[i + 1][0][1]:
                processed[int(raw_level1[i][0][1])] = MetaDataProcessor.process_log_level2(raw_level1[start:i + 1])
        return processed

    @staticmethod
    def process_log_level2(raw_level2):
        processed = dict()
        # separate by node 2
        start = 0
        for i in range(len(raw_level2)):
            if i == (len(raw_level2) - 1) or raw_level2[i][0][2] != raw_level2[i + 1][0][2]:
                processed[int(raw_level2[i][0][2])] = MetaDataProcessor.process_log_level3(raw_level2[start:i + 1])
                start = i+1
        return processed

    @staticmethod
    def process_log_level3(raw_level3):
        processed = dict()
        # determine the minimum and maximum of index
        processed["min_index"] = int(raw_level3[0][0][3][0])
        processed["max_index"] = int(raw_level3[-1][0][3][1])
        mapping = []
        for p in raw_level3:
            mapping.append((p[0][-1][0], p[1]))
        processed["fileID"] = mapping
        return processed

    def process(self):
        print(f"Processing {self.path}")
        with open(self.path, 'r') as f:
            raw = json.load(f)
        raw = list(raw.items())
        raw = list(map(self.splitter, raw))
        raw.sort(key=lambda item: (item[0][0], item[0][1], item[0][2], item[0][3]))

        # separate sent log from trace log
        watershed = 0
        for i in range(len(raw)):
            if raw[i][0][0] != 'sent':
                watershed = i
                break

        processed = dict()
        processed["emission"] = self.process_log_level1(raw[:watershed])
        processed["reception"] = self.process_log_level1(raw[watershed:])

        # generate output path
        processed_path = self.path.split('/')
        processed_path[-1] = "processed_" + processed_path[-1]
        processed_path = '/'.join(processed_path)
        with open(processed_path, 'w') as f:
            json.dump(processed, f, indent=4)
        print(f"Done. Successfully output to {processed_path}")


if __name__ == "__main__" :
    processor = MetaDataProcessor(sys.argv[1])
    processor.process()
