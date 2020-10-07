
"""
En este archivo se contienen los base64 de el logo de la ventana y el popup animado
"""
def obtener_logo():
    """
    Tuve que crear esta funcion para poder respetar las Pep.
    De verdad, es larguisimo el string para el iconito
    """
    cadena = b'iVBORw0KGgoAAAANSUhEUgAAAEkAAABJCAYAAABxcwvcAAAACXBIWXMAAAsTAA\
    ALEwEAmpwYAAAAIGNIUk0AAHolAACAgwAA+f8AAIDpAAB1MAAA6mAAADqYAAAXb5JfxUYAAAS\
    2SURBVHja7Jw/bBRHFIe/tXwKnIRQTIEgGwGRQL4IIgFCchpMQcGfigLSXJEWOY3BDhIFvVPQ\
    IFoarqOgIkoiClsIBVDcOCffwUlGkRwllSVksJAoTHGzsF5mZnd2Z/aOu3nSSqfZ29vd377vv\
    Zk3ewNq+xr4CXgErAObA7j9DzwQ9xliYHuBhwMqStr2UNy/1s4NqTjJ7VxWgZ4D3wPbGGzbJu\
    7zeZpQYeILs0DAcFkAzCR02BKnnsV2XGO4bTamxV9R4/4EYsGQixQArZgmBwCuxhpO4g0RoyJ\
    NZgAexxq2e30+BPNIk8cAr2IN3j5apMl6kBAn8NpsEQmAEa9FunmRvEh2bNTS71Q1w5e3wIbD\
    31fZOvDOdhQvkt3mUwaMRRPCXIHB6l2gbloKSepSVKRqhgut9VCk+DZvcC0fjrMRkyYzfOdMn\
    4SXSWBZiB6Uidt8xqcY9IEnJTEMysCtqnBp28jNKW5yTLGFwIT4jk6os2WIdFZxYtnFTVsWaS\
    7jsWMp3l5xLZLs5FXxFG0iV0SkaLilEmrCZeCuSoL2gugTLSqOGe/hOKyuKYs463FPKp44ohP\
    X6LMstwq8lLQfc5ndVKhFZhO5orilZUknuIUa1CLrN+RU9tIVbqc0qNHHyMkmHu+5wm0lBTXb\
    yNnArWLYVyqEW4iYQUi4rGykv9RHyJ1WtD91gZsMtRuK726IWNVr5GrAr5L2BrDmAjcZaqFhr\
    9wUuby4BZrzq0LEJ7qMWkJtVXPMgga5VsEgPKbYd0h0Em9qjv/WpBho4kl1ydOo5+xTTRf0pL\
    zbSsbBdu6xmylqtpCzJVJdM6C1IlKoeCpFqpe1EkRaEV2RiiHOuboAJlmtn7LcAeCCjRFymic\
    FiqdkUlwvglyW7BaI66lrPKri0pPGFWOeVYOT/u24Y7kprqchMpfMo+7k+eGsIsmwuGWpVPGj\
    A8RaCqHqmiJbIdwC7NWsVShULOBmEvArtnFT4bBMvhkKmR13FLRVQv5gG7cyMtCUo99dA36Rt\
    N817RLocAso793piqNSyZimY2kFtzJLGsf71ZtGc6C2kKUGk2IXJQPlKeCJw9j0syI2NYrgZj\
    OrFc1yNiqTppkuE24q1NoWRJovGblCmU4nkqyTdwU7b+n+W3KWi2JTI29skuGmKppPWLzoaQP\
    3tzXvVjPIdKm4qdx+0aJIv/UAuZaiGqH1phEDt29g8R1ETWxziRzA5TyxKYlbGaiZImcLt3ji\
    SDuvFrcyUOslcsbe5P82oSfMqJ401OZF8iJ5kbxIXiQvkhfJi+RNbqPAf8CeQbqpw+MHa8BOM\
    ZTaTXf6+xXwD7BP7FsCvgNotjtPJCORyF6PsHX6eSDWBWi2Oy26M8Y7gCPAC+B6s93ZEPu+pP\
    uK9SIwdXj8YHJA/UXs89II8Ees4cSAeFIAhM12Z43u2zBV4HexL6RbU9olBtK3JVWHo7HP9wO\
    6a5VEc/RtunPom5+5SHPAfeFBh2K7VunO1PwpPh8BdjXbnUYCtWU+1vi/iXbEV72ZHfI4LV31\
    Bvz6SZEHaddPAjiPX4krfv/nVQdcxK/ntglcSlP2K4Z7dUCj9QP2C0YfAW8GVJQ34v5mxP1K7\
    f0A2wJqfDSaFUAAAAAASUVORK5CYII='
    return cadena

def obtener_gif():
    cubito = b'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'
    return cubito