import spider
class calcSim:

    def urlSim(self, url , query):

        result = 0
        hits = 0
        for i in query:
            for x in url:
                if query[i] == url[x]: hits += 1
        
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
