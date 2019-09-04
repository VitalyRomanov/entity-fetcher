import csv
class LentaReader:
    def __init__(self, path):
        self._fobj = open(path, "r")
        self._schema = "tags,text,title,topic,url".split(",")
        self._fobj.readline()

    def readNews(self):
        line = self._fobj.readline().strip()

        if line:
            return dict(zip(self._schema, list(csv.reader([line]))[0]))
        else:
            # return None
            line = self._fobj.readline().strip()

            if line:
                return dict(zip(self._schema, list(csv.reader([line]))[0]))
            else:
                return None

