from Services.dal import DAL
from Repositories.userRepository import UserRepository

class LogStash():
    repository: UserRepository

    def __init__(self,dataAccessLayer:DAL) -> None:
        self.repository=UserRepository(dataAccessLayer)

    def createUser(self,regdate:str,regtime:str)->int:
        return self.repository.createUser(regdate,regtime)
        
    def newChangeWeight(self,regtime:str,chagedweight:int,userID:int):
        # print("\n>>>>>>>>>>>>>changed weight is: " + str(chagedweight))
        return self.repository.newChangeWeight(regtime,chagedweight,userID)

    def newAdminLog(self, userID: str, adminBarcode: str, regtime: str):
        return self.repository.newAdminLog(userID,adminBarcode,regtime)

    def peymentLog(self,userID:str,adminBarcode:str,regtime:str):
        return self.repository.peymentLog(userID,adminBarcode,regtime)

    def newChangeState(self,regtime:str,state:int,userID:int):
        # print("\n>>>>>>>>>>>>>new State is: " + str(state))
        return self.repository.newChangeState(regtime,state,userID)


    def newChangeBarcode(self,regtime:str,barcode:str,userID:int):
        # print("\n>>>>>>>>>>>>>new barcode is: " + barcode)
        return self.repository.newChangeBarcode(regtime,barcode,userID)

    def printLog(self,userID:int):
        self.repository.execLog(userID)

    def clearLog(self):
        self.repository.clearLog()

    def suspendedFactorCreated(self,userID:int,suspendedFactorID:str):
        return self.repository.suspendedFactorCreated(userID,suspendedFactorID)

    def factorCreated(self,userID:int,factorID:str):
        return self.repository.factorCreated(userID,factorID)


    def rate(self,userID:int,rate:1):
        return self.repository.rate(userID,rate)


    def factorListCreate(self,userID:int,count:int,barcode:str,price:int,finalPrice:int):
        return self.repository.factorListCreate(userID,count,barcode,price,finalPrice)


