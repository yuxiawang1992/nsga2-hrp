from metrics.hvr import HVR, HV

class HospitalMetrics():
    def HV(self,front):
        return HV([3,3])(front)
        
    def HVR(self,front):
        return HVR([3,3],8 + 1/3)(front)