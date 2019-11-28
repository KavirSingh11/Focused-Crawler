class calcSim:

    def urlSim(self, url , query):
        hits = 0
        for i in query:
            for x in url:
                if i == x: hits += 1
        
        if hits > 2: return True
        else: return False
        

    def calcIDFValues(self):
        pass

    def calcTFValues(self):
        pass

    def calcWeightVector(self):
        pass

    def calcCosineSim(self):
        pass
