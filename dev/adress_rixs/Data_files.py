class Data_files():

    def __init__(self,path,base):
        self.path = path.replace('\\','/')
        self.base = base
        self.runNums = []
        self.fileList = {}

    def make_name(self,runNum):
        fileName = f"{self.path}/{self.base}_{runNum:04d}"
        detectorList = {}
        for i in range(3):
            detectorList[i] = f'{fileName}_d{i+1:d}.h5'
        return detectorList

    def make_list(self,numberString):
        runNums = []
        splits = numberString.split(',')
        for sp in splits:
            isRange = sp.find('-')!=-1
            if isRange:
                spSplits = sp.split('-')
                startNumber = int(spSplits[0])
                endNumber = int(spSplits[1])
                if startNumber>endNumber:
                    numbers = [int(x) for x in range(startNumber,endNumber-1,-1)]    
                else:
                    numbers = [int(x) for x in range(startNumber,endNumber+1)] 
            else:
                numbers = [int(sp)]
            runNums = runNums + numbers
        return runNums

    def load(self,numberString):
        self.runNums = self.runNums + self.make_list(numberString)

        for runNum in self.runNums:
            self.fileList[runNum] = self.make_name(runNum)

