from openpyxl import load_workbook


def parse_xlsx_list(filename, worksheet, columnname):
    wb = load_workbook(filename)
    result = []
    for site in wb[worksheet][columnname]:
        result.append(site.value)
    return result


class SiteList:
    index = -1
    sites = []

    def __init__(self, config):
        if config['file_type'] == 'xlsx':
            self.sites = parse_xlsx_list(config['file_name'], config['worksheet'], config['column'])

    def __iter__(self):
        return self

    def reset(self):
        self.index = -1

    def hasNext(self):
        return self.index < len(self.sites) - 1

    def next(self):
        self.index += 1
        if self.hasNext():
            return self.sites[self.index]
        else:
            raise StopIteration

    def get(self, index):
        if index < len(self.sites):
            return self.sites[index]
        else:
            return -1