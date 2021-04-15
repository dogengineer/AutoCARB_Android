class MachError(Exception):
    pass

class HighHumidityError(Exception):
    pass

class HighPressureError(Exception):
    pass

class DeltaPressureValueError(Exception):
    pass

class NegativeValuesError(Exception):
    pass

class SubAbsoluteTempError(Exception):
    pass

class HighJetDiameterError(Exception):
    pass

class HighJetLengthError(Exception):
    pass

#---------------------------------------------

class DeltaPressureError(Exception):
    pass

class HighDeltaPressureError(Exception):
    pass

class IncompressibleAirDischargeCoefficientError(Exception):
    pass

class ForceDefectCoefficientIncompressibleError(Exception):
    pass