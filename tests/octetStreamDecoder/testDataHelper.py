import csv
from datetime import datetime


def convertToTestDataList(testDataAsString: str) -> []:
    data_list = []

    for line in testDataAsString.strip().splitlines():
        value, error, start, end, type_str = [x.strip() for x in line.split(",")]

        if error or type_str != 'data':
            continue

        data_list.append({
            "value": int(value),
            "start": datetime.fromisoformat(start),
            "end": datetime.fromisoformat(end),
        })

    return data_list


def getTestDataListFromFile(filename: str):
    data_list = []
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            value, error, start, end, type_str = [col.strip() for col in row]

            if error or type_str != 'data':
                continue

            data_list.append({
                "value": int(value),
                "start": datetime.fromisoformat(start),
                "end": datetime.fromisoformat(end),
            })

    return data_list
