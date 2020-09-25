import requests

class CriticalPower:

    data = []
    pos = []
    table = []

    def __init__(self, data, pos, table):
        self.data = data
        self.pos = pos
        self.table = table

    @staticmethod
    def fromResponse(response):
        data = response["data"]
        pos = response["pos"]
        table = response["table"]
        return CriticalPower(data, pos, table)

class ZwiftPowerAnalysis:
    criticalPower = None
    fileIds = []
    names = []
    id = ""

    def __init__(self, id, criticalPower, fileIds, names):
        self.id = id
        self.criticalPower = criticalPower
        self.fileIds = fileIds
        self.names = names

    @staticmethod
    def fromResponse(response, id):
        criticalPower = CriticalPower.fromResponse(response["critical_power"])
        fileIds = response["file_ids"]
        names = response["names"]
        return ZwiftPowerAnalysis(id, criticalPower, fileIds, names)

    def toRows(self):
        rows = []
        for i in range(len(self.criticalPower.data)):
            data = self.criticalPower.data[i]
            baseRow = [str(id), self.names[i]]
            for dataPoint in data:
                baseRow.append(dataPoint["y"])
            rows.append(baseRow)
        return rows
        

def getData(id):
    return requests.get("https://www.zwiftpower.com/api3.php?do=set_analysis&set_id=" + str(id), headers={"User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"})

id = 57253
data = getData(id)
zwiftPowerAnalysis = ZwiftPowerAnalysis.fromResponse(data.json(), id)
print(zwiftPowerAnalysis.toRows())