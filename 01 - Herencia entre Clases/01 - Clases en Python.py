# Definir clase
class CuentaBancaria:
    
    """
    Esta clase representa una cuenta bancaria.
    """
    
    def __init__(self, titular: str, saldo_inicial: float = 0.0) -> None:
        
        """
        Método constructor para inicializar una cuenta bancaria.
        
        Args:
            titular (str): El titular de la cuenta bancaria.
            saldo_inicial (float, opcional): El saldo inicial de la cuenta bancaria, por defecto es 0.0.
        """
        
        # Atributos
        self.titular = titular
        self.__saldo = saldo_inicial # Atributo Privado
        
        
    def __str__(self):
        return f"Cuenta bancaria de {self.titular}"
    
    
    def depositar(self, cantidad: float):
        
        """
        Método para depositar dinero en la cuenta bancaria.
        
        Args:
            cantidad (float): La cantidad a depositar
        """
        
        self.__saldo += cantidad
        print(f"Se han depositado ${cantidad} en la cuenta.")
        
        
    def retirar(self, cantidad: float):
        
        """
        Método para retirar dinero de la cuenta banacaria.
        
        Args:
            cantidad (float): La cantidad a retirar de la cuenta
        """
        
        if cantidad <= self.__saldo:
            self.__saldo -= cantidad
            print(f"Se ha retirado ${cantidad} de la cuenta")
        else:
            print("Fondos son insuficientes")
            
        
    def consultar_saldo(self):
        
        """
        Método para consultar el saldo con el que cuenta el cliente en su cuenta bancaria.
        """
        
        print(f"Saldo actual de la cuenta de {self.titular}: ${self.__saldo}")
        
        
# Crear instancias de la clase CuentaBancaria
cuenta1 = CuentaBancaria("Juan Pérez", 1000)
print(cuenta1)
cuenta2 = CuentaBancaria("María González", 1500)
print(cuenta2)   

# Realizar operaciones en las cuentas
cuenta1.depositar(500)
cuenta1.retirar(200)
cuenta1.consultar_saldo()
        
cuenta2.consultar_saldo()

# Intentar acceder a los atributos privados
try:
    print(cuenta1.__saldo)        
except:
    print("No se puede acceder a ese atributo porque es privado")
        
# Recordatorio:
#   - Las clases en Python son plantillas para la creación de objetos que encapsulan datos y comportamientos relacionados,
#     promoviendo la reutilización de código y una estructura organizada.
#   - "Self" en Python es una referencia al objeto actual dentro de una clase, permitiendo el acceso a sus atributos
#      y métodos para realizar operaciones específicas dentro de los métodos de la clase.
