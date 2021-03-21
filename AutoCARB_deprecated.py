from AutoCARB import *

##############################################################################################

#METODO DI NEWTON IMPLEMENTATO PER IL CALCOLO DEL COEFFICIENTE DI EFFLUSSO DELL'ARIA

def MN(Tamb,pamb,deltap,d1,d3,d2max,d2min,C,r_n0):
    """ 
    Metodo di Newton implementato per il calcolo del coefficiente di efflusso dell'aria
    
    Args:
        Tamb: temperatura ambiente
        pamb: pressione ambiente
        deltap: pressione differenziale tra la pressione ambiente e la pressione nella sezione 3
        d3: diametro della sezione 3
        d2max: diametro massimo della sezione di gola
        d2min: diametro minimo della sezione di gola
    
    Returns:
        valore iterato di rn
    """      
    Re = numeroReynolds(Tamb,pamb,deltap,d3,d2max,d2min)
    P2t = PressioneAriaTeorica2(Tamb,pamb,deltap,d3,d2max,d2min)
    T2t = TemperaturaTeoricaAria2(Tamb,pamb,deltap,d3,d2max,d2min)           
    d2medio = ((d2max+d2min)/2)
    
    #coefficiente dell'aria incomprimibile calcolata con neutrium
    #https://neutrium.net/fluid-flow/discharge-coefficient-for-nozzles-and-orifices/
    coeffAir_i = 0.9975-((6.53*np.sqrt(d2medio/d1))/np.sqrt(Re))
    C_i=coeffAir_i
    
    #esponente della trasformazione adiabatica
    gamma = RapportoCaloreAria(T2t)
    
    #rapporto tra la pressione di gola e la pressione atmosferica            
    r_a = P2t/pamb
    
    #equazione 6 del paper(Force defect coefficient fluido incomprimibile)
    f_i=1/C_i-1/(2*C_i**2) 
    
    #equazione 16 del paper
    k = np.sqrt(2*f_i) 
    
    #primo passo del metodo di Newton
    #r_n(1) = r_n0
    
    #ciclo del metodo di Newton 
    for i in range(r_n0, Constants.iterAir):      
        
        #scrivo la funzione con variabile r_n
        z_= lambda i : r_n(i)**(2/gamma)*(1-r_n(i)**((gamma-1)/gamma))-(k*C)^2*r_a**(2/gamma) * \
                       (1-r_a**((gamma-1)/gamma))
        
        #scrivo il valore della derivata della funzione precedente 
        z1_ = lambda i : (2/gamma)*r_n(i)**((2-gamma)/gamma)-((gamma+1)/gamma)*r_n(i)**(1/gamma)

        #scrivo la formula di NEWTON
        r_n = lambda i : r_n(i-1)-z_(i-1)/z1_(i-1)

        #impongo che se non viene rispettato un certo valore minimo di errore
        #ricomincia da capo il ciclo for
        if abs(r_n(i+1)-r_n(i)) > (1e-10):
            continue
        else:
            break
            
    return r_n(i+1)