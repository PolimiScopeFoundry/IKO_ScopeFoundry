"""
****************************************
Created on Wed Oct 15 16:45:26 2025
@authors: Martina Riva. Politecnico di Milano

"""

from ScopeFoundry import BaseMicroscopeApp

class IKO_app(BaseMicroscopeApp):
    

    name = 'IKO_app'
    
    def setup(self):
        
        #Add hardware components
        print("Adding Hardware Components")
        from IKO_Hardware import IKO_HW
        self.add_hardware(IKO_HW(self))
           

        self.ui.show()
        self.ui.activateWindow()


if __name__ == '__main__':
    import sys
    
    app = IKO_app(sys.argv)
    sys.exit(app.exec_())
