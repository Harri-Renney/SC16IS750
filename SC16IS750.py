import smbus
from enum import IntEnum

class SC16IS750:
    self.DEVICE_ADDRESS = 0x9A
    CrystalFrequency = 0
    class registers(IntEnum):
        RHR= 0x00       # Receive Holding Register (R)
        THR= 0x00       # Transmit Holding Register (W)
        IER= 0x01       # Interrupt Enable Register (R/W)
        FCR= 0x02       # FIFO Control Register (W)
        IIR= 0x02       # Interrupt Identification Register (R)
        LCR= 0x03       # Line Control Register (R/W)
        MCR= 0x04       # Modem Control Register (R/W)
        LSR= 0x05       # Line Status Register (R)
        MSR= 0x06       # Modem Status Register (R)
        SPR= 0x07       # Scratchpad Register (R/W)
        TCR= 0x06       # Transmission Control Register (R/W)
        TLR= 0x07       # Trigger Level Register (R/W)
        TXLVL = 0x08    # Transmit FIFO Level Register (R)
        RXLVL = 0x09    # Receive FIFO Level Register (R)
        IODIR= 0x0A     # I/O pin Direction Register (R/W)
        IOSTATE= 0x0B   # I/O pin States Register (R)
        IOINTENA= 0x0C  # I/O Interrupt Enable Register (R/W)
        IOCONTROL= 0x0E # I/O pins Control Register (R/W)
        EFCR= 0x0F      # Extra Features Register (R/W)

        # -- Special Register Set (Requires LCR[7] = 1 & LCR != 0xBF to use)
        DLL= 0x00       # Divisor Latch LSB (R/W)
        DLH= 0x01       # Divisor Latch MSB (R/W)

        # -- Enhanced Register Set (Requires LCR = 0xBF to use)
        EFR= 0x02       # Enhanced Feature Register (R/W)
        XON1= 0x04      # XOn1 (R/W)
        XON2= 0x05      # XOn2 (R/W)
        XOFF1= 0x06     # XOff1 (R/W)
        XOFF2= 0x07     # XOff2 (R/W)

    def init(self, crystalFrequency, deviceaddress=0x9A):
        print("Initalising SC16IS750.")
        self.DEVICE_ADDRESS = deviceaddress
        self.bus = smbus.SMBus(1)
        self.crystalFrequency = crystalFrequency
#        def __init__():

    def readRegister(self, registerAddress):
        shiftedDeviceAddress = self.DEVICE_ADDRESS >> 1
        shiftedRegisterAddress = registerAddress << 3
        registerReadValue = self.bus.read_byte_data(shiftedDeviceAddress, shiftedRegisterAddress)
        return registerReadValue

    def writeRegister(self, registerAddress, data):
        shiftedDeviceAddress = self.DEVICE_ADDRESS >> 1
        shiftedRegisterAddress = registerAddress << 3
        self.bus.write_byte_data(shiftedDeviceAddress, shiftedRegisterAddress, data)

    ##Set the desired baudrate of chips UART##
    def setBaudrate(self, baudrate):
        clockDivisor = (self.readRegister(self.registers.MCR) & 0b10000000) >> 7
        if(clockDivisor == 0):
            prescaler = 1
        elif(clockDivisor == 1):
            prescaler = 4
        divisor = int((self.crystalFrequency / prescaler) / (baudrate * 16))
        
        lowerDivisor = (divisor & 0xFF)
        higherDivisor = (divisor & 0xFF00) >> 8

        self.setRegisterBit(self.registers.LCR, 7)

        self.writeRegister(self.registers.DLL, lowerDivisor)
        self.writeRegister(self.registers.DLH, higherDivisor)

        self.unsetRegisterBit(self.registers.LCR, 7)

    ##Set the desired UART attributes##
    def setUARTAttributes(self, dataBits, parityType, stopBits):
        #Calculate bits for LCR register#
        print("Setting UART attributes.")

    ##Set the bit in position passed##
    def setRegisterBit(self, registerAddress, registerBit):
        current = self.readRegister(registerAddress)
        updated = current | (1 << registerBit)
        self.writeRegister(registerAddress, updated)

    ##Unset the bit in position passed##
    def unsetRegisterBit(self, registerAddress, registerBit):
        current = self.readRegister(registerAddress)
        updated = current & ~(1 << registerBit)
        self.writeRegister(registerAddress, updated)

    ##Checks if any data in FIFO buffer##
    def isDataWaiting(self):
        register = self.readRegister(self.registers.LSR)
        isWaiting = register & 0b1
        if(isWaiting):
            return True
        return False

    ##Checks number of bytes waiting in FIFO buffer##
    def dataWaiting(self):
        return self.readRegister(self.registers.RXLVL)
        
    ##Writes to Scratch register and checks successful##
    def testChip(self):
        self.writeRegister(self.registers.SPR, 0xFF)
        if(self.readRegister(self.registers.SPR) != 0xFF):
            return False
        return True            









        
