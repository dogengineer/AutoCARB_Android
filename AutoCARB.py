import numpy as np

class Constants:
    g = 9.80655  
    R = 287.05
    k2c = 273.15
    pi = np.pi
    iterazioni = 200


def temperaturaambiente_Kelvin(Tamb):
    return Tamb + Constants.k2c

def cp_air_interp(Tamb):
    """ 
    Calore specifico a pressione costante dell'aria calcolato alla temperatura ambiente
    
    Args:
        Tamb: temperatura ambiente
    
    Returns:
        calore specifico a pressione costante dell'aria (è un polinomio interpolante)
    """
    TambK = temperaturaambiente_Kelvin(Tamb)
    coeff = [-2.15726618016776e-22, 5.01984774779347e-18, -4.70708079188254e-14,
              2.26347904024044e-10, -5.81600604212894e-07, 0.000724060127601295,
             -0.206195541977422, 1023.70412983013]
    
    return np.polyval(coeff, TambK)


def pressioneAria3(pamb, deltap):
    """ 
    pressione dell'aria che passa nella sezione 3 (dato ricavatoesclusivamente dalle misure) 
    
    Args:
        pamb: pressione ambiente
        deltap: pressione differenziale tra la pressione ambiente e la pressione nella sezione 3
    
    Returns:
        Pressione dell'aria nella sezione 3
    """
    return pamb - deltap


def RapportoCaloreAria(Tamb):
    """ 
    esponente della trasformazione adiabatica

    Args:
        Tamb: temperatura ambiente
    
    Returns:
        coefficiente k
    """
    cp = cp_air_interp(Tamb)            
    return cp / (cp - Constants.R )

        
#ci serve per calcolare la densità dell'aria nella sezione 2
def densitAir1(Tamb,pamb):
    """ 
    Densità dell'aria che passa nella SEZIONE 1 (quella situata all'inizio del convergente)
    
    Args:
        Tamb: temperatura ambiente
        pamb: pressione ambiente
    
    Returns:
        Densità dell'aria nella sezione 1, questa quantità è lecito considerarla solo a temperatura ambiente
        perché essa viene considerata solo per quanto riguarda la quantità di aria aspirata
    """            
    return pamb/((Constants.R)*(Tamb+(Constants.k2c)))
        

def UmiditAssoluta(Tamb,pamb,phi):
    """ 
    Umidità assoluta dell'aria
    
    Args:
        Tamb: temperatura ambiente
        pamb: pressione ambiente
        phi: umidità relativa
    
    Returns:
        Umidità assoluta
    """
    if Tamb>50:
        return 0 #this passage is needed to solve an interpolation error
    psat = ( 0.006228+0.000782638*Tamb-0.000181025*Tamb**2+0.0000479501*Tamb**3-0.0000064238*Tamb**4+0.000000538869*Tamb**5-0.0000000297812*Tamb**6+0.00000000111524*Tamb**7-0.000000000028466*Tamb**8+0.000000000000487735*Tamb**9-5.36485E-015*Tamb**10+3.42159E-017*Tamb**11-9.61488E-020*Tamb**12)*98100
    #pressione parziale del vapore nel miscuglio
    PvapMisc=(phi*psat)/100
    return 0.622*(PvapMisc/(pamb-PvapMisc))


def areaSezione2(d2max,d2min):
    """ 
    valore dell'area della sezione 2
    
    Args:
        d2max: diametro massimo della sezione di gola
        d2min: diametro minimo della sezione di gola
    
    Returns:
        Area della sezione di gola
    """   
    return (Constants.pi/4)*d2max*d2min


def areaSezione3(d3):
    """ 
    valore dell'area della sezione 3
    
    Args:
        d3: diametro della sezione 3
    
    Returns:
        Area della sezione 3
    """
    return (Constants.pi/4)*d3**2


#NEW NEW
def TemperaturaTeoricaAria3(Tamb,pamb,deltap):
    """ 
    temperatura teorica dell'aria che passa nella sezione 3
    
    Args:
        Tamb: temperatura ambiente
        pamb: pressione ambiente
        deltap: pressione differenziale tra la pressione ambiente e la pressione nella sezione 3
    
    Returns:
        Temperatura in prossimità della sezione 3
    """
    P3 = pressioneAria3(pamb,deltap)
    k = RapportoCaloreAria(Tamb)
    
    return ((Tamb+(Constants.k2c))*(P3/pamb)**((k-1)/k))


def velocitaSez3(Tamb,pamb,deltap):           
    """ 
    velocità teorica dell'aria che passa nella sezione 3

    Args:
        Tamb: temperatura ambiente
        pamb: pressione ambiente
        deltap: pressione differenziale tra la pressione ambiente e la pressione nella sezione 3
    
    Returns:
        Velocità in prossimità della sezione 3
    """
    P3 = pressioneAria3(pamb,deltap)
    T3 = TemperaturaTeoricaAria3(Tamb,pamb,deltap)
    k = RapportoCaloreAria(T3)
    
    return np.sqrt(k*(Constants.R)*(Tamb+(Constants.k2c)))*np.sqrt((2/(k-1))*(1-(P3/pamb)**((k-1)/k)))


def velocitaTeoricaSez2(Tamb,pamb,deltap,d3,d2max,d2min):
    """ 
    velocità teorica dell'aria che passa nella sezione 2

    Args:
        Tamb: temperatura ambiente
        pamb: pressione ambiente
        deltap: pressione differenziale tra la pressione ambiente e la pressione nella sezione 3
        d3: diametro della sezione 3
        d2max: diametro massimo della sezione di gola
        d2min: diametro minimo della sezione di gola
    
    Returns:
        Velocità in prossimità della sezione 3
    """
    cTret = velocitaSez3(Tamb,pamb,deltap)
    omegaDue = areaSezione2(d2max,d2min)
    omegaTre = areaSezione3(d3)
    
    return (omegaTre/omegaDue)*cTret      

    
def PressioneAriaTeorica2(Tamb,pamb,deltap,d3,d2max,d2min):
    """ 
    pressione teorica dell'aria che passa nella sezione 2
    
    Args:
        Tamb: temperatura ambiente
        pamb: pressione ambiente
        deltap: pressione differenziale tra la pressione ambiente e la pressione nella sezione 3
        d3: diametro della sezione 3
        d2max: diametro massimo della sezione di gola
        d2min: diametro minimo della sezione di gola
    
    Returns:
        Pressione in prossimità della sezione 2, (kappa è approssimato perché calcolato a Tamb)
    """  
    cDuet = velocitaTeoricaSez2(Tamb,pamb,deltap,d3,d2max,d2min)
    k = RapportoCaloreAria(Tamb)
    
    return pamb*(1-(((k-1)*((cDuet**2)/2))/(k*(Constants.R)*(Tamb+(Constants.k2c)))))**(k/(k-1))
      

def TemperaturaTeoricaAria2(Tamb,pamb,deltap,d3,d2max,d2min):
    """ 
    temperatura teorica dell'aria che passa nella sezione 2
    
    Args:
        Tamb: temperatura ambiente
        pamb: pressione ambiente
        deltap: pressione differenziale tra la pressione ambiente e la pressione nella sezione 3
        d3: diametro della sezione 3
        d2max: diametro massimo della sezione di gola
        d2min: diametro minimo della sezione di gola
    
    Returns:
        Temperatura in prossimità della sezione 2, (kappa è approssimato perché calcolato a Tamb)
    """
    P2t = PressioneAriaTeorica2(Tamb,pamb,deltap,d3,d2max,d2min)
    k = RapportoCaloreAria(Tamb)
    
    return ((Tamb+(Constants.k2c))*(P2t/pamb)**((k-1)/k))


def NumeroMach(Tamb,pamb,deltap,d3,d2max,d2min):
    """ 
    numero di Mach nella sezione 2 (sezione di gola)
    
    Args:
        Tamb: temperatura ambiente
        pamb: pressione ambiente
        deltap: pressione differenziale tra la pressione ambiente e la pressione nella sezione 3
        d3: diametro della sezione 3
        d2max: diametro massimo della sezione di gola
        d2min: diametro minimo della sezione di gola
    
    Returns:
        numero di Mach
    """
    T2t = TemperaturaTeoricaAria2(Tamb,pamb,deltap,d3,d2max,d2min)
    k = RapportoCaloreAria(T2t)
    Cs = np.sqrt(k*Constants.R*T2t)
    cDuet = velocitaTeoricaSez2(Tamb,pamb,deltap,d3,d2max,d2min)
    
    return cDuet/Cs            
        

def DensitaAria2(Tamb,pamb,deltap,d3,d2max,d2min):
    """ 
    densità dell'aria che passa nella sezione 2
    
    Args:
        Tamb: temperatura ambiente
        pamb: pressione ambiente
        deltap: pressione differenziale tra la pressione ambiente e la pressione nella sezione 3
        d3: diametro della sezione 3
        d2max: diametro massimo della sezione di gola
        d2min: diametro minimo della sezione di gola
    
    Returns:
        densità nella sezione 2
    """

    P2t = PressioneAriaTeorica2(Tamb,pamb,deltap,d3,d2max,d2min)
    RhoA = densitAir1(Tamb,pamb)            
    T2t = TemperaturaTeoricaAria2(Tamb,pamb,deltap,d3,d2max,d2min)
    k = RapportoCaloreAria(T2t)            
    
    return RhoA*(pamb/P2t)**(-1/k)

  
def viscositaDinamicaAir(Tamb,pamb,deltap,d3,d2max,d2min):
    """ 
    viscosità dinamica dell'aria che passa nella sezione 2
    
    Args:
        Tamb: temperatura ambiente
        pamb: pressione ambiente
        deltap: pressione differenziale tra la pressione ambiente e la pressione nella sezione 3
        d3: diametro della sezione 3
        d2max: diametro massimo della sezione di gola
        d2min: diametro minimo della sezione di gola
    
    Returns:
        viscosità nella sezione 2 (è un polinomio interpolante)
    """
    T2t = TemperaturaTeoricaAria2(Tamb,pamb,deltap,d3,d2max,d2min)

    return 0.0000178*(T2t/288.15)**(1/3)*((288.15+110)/(T2t+110))
    

def numeroReynolds(Tamb,pamb,deltap,d3,d2max,d2min):
    """ 
    numero di Reynolds dell'aria che passa nella sezione 2
    
    Args:
        Tamb: temperatura ambiente
        pamb: pressione ambiente
        deltap: pressione differenziale tra la pressione ambiente e la pressione nella sezione 3
        d3: diametro della sezione 3
        d2max: diametro massimo della sezione di gola
        d2min: diametro minimo della sezione di gola
    
    Returns:
        numero di Reynolds
    """
    cDuet = velocitaTeoricaSez2(Tamb,pamb,deltap,d3,d2max,d2min)
    RhoA2 = DensitaAria2(Tamb,pamb,deltap,d3,d2max,d2min)
    muAir = viscositaDinamicaAir(Tamb,pamb,deltap,d3,d2max,d2min)            
    
    return (cDuet*RhoA2*((d2max+d2min)/2))/muAir


def newton(f, Df, x0, epsilon = 1e-10, epserr = 1e-10, max_iter = Constants.iterazioni):
    '''Approximate solution of f(x)=0 by Newton's method.

    Parameters
    ----------
    f : function
        Function for which we are searching for a solution f(x)=0.
    Df : function
        Derivative of f(x).
    x0 : number
        Initial guess for a solution f(x)=0.
    epsilon : number
        Stopping criteria is abs(f(x)) < epsilon.
    max_iter : integer
        Maximum number of iterations of Newton's method.

    Returns
    -------
    xn : number
        Implement Newton's method: compute the linear approximation
        of f(x) at xn and find x intercept by the formula
            x = xn - f(xn)/Df(xn)
        Continue until abs(f(xn)) < epsilon and return xn.
        If Df(xn) == 0, return None. If the number of iterations
        exceeds max_iter, then return None.

    Examples
    --------
    >>> f = lambda x: x**2 - x - 1
    >>> Df = lambda x: 2*x - 1
    >>> newton(f,Df,1,1e-8,10)
    Found solution after 5 iterations.
    1.618033988749989
    '''
    xn = x0
    fxn = f(x0)
    for _ in range(0,max_iter):
        fxn_old, fxn = fxn, f(xn)
        if abs(fxn) < epsilon and abs(fxn_old-fxn) < epserr:
            # print('Found solution after',n,'iterations.')
            return xn
        Dfxn = Df(xn)
        if Dfxn == 0:
            # print('Zero derivative. No solution found.')
            return None
        xn = xn - fxn/Dfxn
    # print('Exceeded maximum iterations. No solution found.')
    return None


def Coefficiente_efflusso_aria(Tamb, pamb, deltap, d1, d3, d2max, d2min, r_n0 = 1):
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
    C_i = 0.9975-((6.53*np.sqrt(d2medio/d1))/np.sqrt(Re))

    #esponente della trasformazione adiabatica
    gamma = RapportoCaloreAria(T2t)
    
    #rapporto tra la pressione di gola e la pressione atmosferica            
    r_a = P2t/pamb
    
    #equazione 6 del paper(Force defect coefficient fluido incomprimibile)
    f_i=1/C_i-1/(2*C_i**2) 
    
    #equazione 16 del paper
    k = np.sqrt(2*f_i)

    #first guess
    C1 = 0.8 
   
    fx = lambda x : x**(2/gamma)*(1-x**((gamma-1)/gamma))-(k*C1)**2*r_a**(2/gamma) * \
                       (1-r_a**((gamma-1)/gamma))
        
        #scrivo il valore della derivata della funzione precedente 
    Dfx = lambda x : (2/gamma)*x**((2-gamma)/gamma)-((gamma+1)/gamma)*x**(1/gamma)
    
    iters=Constants.iterazioni

    #creazione vettori
    r_n_first = list(range(iters))
    f_loop = list(range(iters))
    C_loop = list(range(iters))
    r_n = list(range(iters))
    C = list(range(iters))
    f_loop_2 = list(range(iters))
    err = list(range(iters))

    #Il seguente ciclo "for" controlla che il punto iniziale x0 usato in newton sia corretto in quanto
        # la funzione fx ha due "zeri". In questo caso è necessario trovare il secondo zero
    x0 = 0.1 #first guess for newton
    for n in range(0,iters-1):
        r_n_first[n] = newton(fx,Dfx,x0)
        if r_n_first[n] is None:
            x0 = x0+0.1
            continue
        f_loop[n] = f_i*(2/r_n_first[n]**(1/k)-(k-1)*(1-r_n_first[n])/(k*\
        r_n_first[n]**(2/k)*(1-r_n_first[n]**((k-1)/k))))

        C_loop[n] = (1-np.sqrt(1-(2*f_loop[n]*(k-1)*(1-r_a)/(k*(1-\
        r_a**((k-1)/k))))))/(2*f_loop[n]*r_a**(1/k))

        if f_loop[n]>0 and C_loop[n]>0 and np.isreal(f_loop[n]) and np.isreal(C_loop[n]):
            r_n_final = r_n_first[n]
            break
        x0 = x0+0.1

    # r_n[0] = newton(fx, Dfx, r_n0)
    r_n[0] = r_n_final

    
    for n in range(0,iters):
        f_loop_2[n] = f_i*(2/r_n[n]**(1/gamma)-(gamma-1)*(1-r_n[n])/(gamma*\
        r_n[n]**(2/gamma)*(1-r_n[n]**((gamma-1)/gamma))))

        C[n] = (1-np.sqrt(1-(2*f_loop_2[n]*(gamma-1)*(1-r_a)/(gamma*(1-\
        r_a**((gamma-1)/gamma))))))/(2*f_loop_2[n]*r_a**(1/gamma))
        
        f2 = lambda r_n: r_n**(2/gamma)*(1-r_n**((gamma-1)/gamma))-(k*C[n])**2*r_a**(2/gamma)*(1-r_a**((gamma-1)/gamma))
        
        Df2 = lambda r_n: (2/gamma)*r_n**((2-gamma)/gamma)-((gamma+1)/gamma)*r_n**(1/gamma)
        
        if n==0:
            r_n[n+1] = newton(f2, Df2, r_n0)
            continue

        err[n] = abs(C[n]-C[n-1])

        if err[n]>1e-6:
            r_n[n+1]= newton(f2, Df2, r_n0)
            continue
        break
        #coeff_air = C[n]
        
        """
        print(coeff_air,'after ',n,'steps')
        if (iters-n)<5:
            print('please consider increasing the n° of iterations')
        """

    return C[n]


def portata_aria(Tamb, pamb, phi, deltap, d1, d3, d2max, d2min, r_n0 = 1):
    """ 
    PORTATA IN MASSA DI ARIA
    
    Args:
        Tamb: temperatura ambiente
        pamb: pressione ambiente
        phi: umidità relativa dell'aria
        deltap: pressione differenziale tra la pressione ambiente e la pressione nella sezione 3
        d3: diametro della sezione 3
        d2max: diametro massimo della sezione di gola
        d2min: diametro minimo della sezione di gola
        C e r_n0: iterati iniziali
    
    Returns:
        portata aria
    """ 
    coeffAir = Coefficiente_efflusso_aria(Tamb, pamb, deltap, d1, d3, d2max, d2min, r_n0 = 1)
    area2 = areaSezione2(d2max,d2min)
    T2t = TemperaturaTeoricaAria2(Tamb,pamb,deltap,d3,d2max,d2min)
    k = RapportoCaloreAria(T2t)
    P2 = PressioneAriaTeorica2(Tamb, pamb, deltap, d3, d2max, d2min)
    Omega = UmiditAssoluta(Tamb, pamb, phi)
    
    return coeffAir*((area2*pamb)/np.sqrt(k*(Constants.R)*(Tamb+(Constants.k2c))))*\
        np.sqrt(((2*k**2)/(k-1))*(P2/pamb)**(2/k)*(1-(P2/pamb)**((k-1)/k)))*(1-Omega)

    

################### BENZINA ###############################################################


def densitBenzina(Tamb):
    """ 
    densità della benzina che scorre nel getto del massimo 
    
    Args:
        Tamb: temperatura ambiente
    
    Returns:
        densità della benzina
    """
    mb=720
    Trif=15
    Kc=0.00096
    
    return mb/(1+Kc*(Tamb-Trif))

        
def pressioneMonteGetto(pamb,Tamb,hc): 
    """ 
    pressione della benzina a monte del getto del massimo 
    
    Args:
        pamb: pressione ambiente
        Tamb: temperatura ambiente
        hc: altezza dal ingresso del getto al pelo libero della benzina nella vaschetta
    
    Returns:
        pressione benzina
    """           
    RhoB = densitBenzina(Tamb)
    
    return pamb+RhoB*(Constants.g)*hc

      
def viscositaCinematicaBenzina(Tamb):
    """ 
    viscosità cinematica della benzina 
    
    Args:
        Tamb: temperatura ambiente
    
    Returns:
        viscosità della benzina
    """
    RhoB = densitBenzina(Tamb)
    
    return RhoB*0.0000008


def areaSezioneGetto(dgetto):
    """ 
    valore dell'area della sezione del getto
    
    Args:
        dgetto: diametro del getto
    
    Returns:
        area della sezione getto
    """

    return (Constants.pi/4)*dgetto**2

       
def velocitaTeoricaBenzina(Tamb,pamb,deltap,d3,d2max,d2min,hc,hd):
    """ 
    velocità teorica della benzina
    
    Args:
        Tamb: temperatura ambiente
        pamb: pressione ambiente
        deltap: pressione differenziale tra la pressione ambiente e la pressione nella sezione 3
        d3: diametro della sezione 3
        d2max: diametro massimo della sezione di gola
        d2min: diametro minimo della sezione di gola
        hc: altezza dal ingresso del getto al pelo libero della benzina nella vaschetta
        hd: altezza dall'uscita del getto all'asse di simmetria del venturi
    
    Returns:
        velocità della benzina
    """
    RhoB = densitBenzina(Tamb)           
    pc = pressioneMonteGetto(pamb,Tamb,hc)
    p2 = PressioneAriaTeorica2(Tamb,pamb,deltap,d3,d2max,d2min)
    pd = p2+RhoB*(Constants.g)*hd
    
    return np.sqrt((2*(pc-pd)/RhoB)-(hd-hc)*(Constants.g))


            
def NumeroDiReynoldsBenzina(Tamb,pamb,deltap,d3,d2max,d2min,hc,hd,dgetto):
    """ 
    velocità teorica della benzina
    
    Args:
        Tamb: temperatura ambiente
        pamb: pressione ambiente
        deltap: pressione differenziale tra la pressione ambiente e la pressione nella sezione 3
        d3: diametro della sezione 3
        d2max: diametro massimo della sezione di gola
        d2min: diametro minimo della sezione di gola
        hc: altezza dal ingresso del getto al pelo libero della benzina nella vaschetta
        hd: altezza dall'uscita del getto all'asse di simmetria del venturi
        dgetto: diametro del getto
    
    Returns:
        numero di Reynolds della benzina
    """
    cDt = velocitaTeoricaBenzina(Tamb,pamb,deltap,d3,d2max,d2min,hc,hd)
    muBenz = viscositaCinematicaBenzina(Tamb)
    RhoB = densitBenzina(Tamb)
    return cDt*RhoB*dgetto/muBenz
        

def coefficiente_attrito_benzina(Tamb,pamb,deltap,d3,d2max,d2min,hc,hd,dgetto):
    """ 
    metodo di Newton implementato per la stima del coefficiente di attrito del getto 
    
    Args:
        Tamb: temperatura ambiente
        pamb: pressione ambiente
        deltap: pressione differenziale tra la pressione ambiente e la pressione nella sezione 3
        d3: diametro della sezione 3
        d2max: diametro massimo della sezione di gola
        d2min: diametro minimo della sezione di gola
        hc: altezza dal ingresso del getto al pelo libero della benzina nella vaschetta
        hd: altezza dall'uscita del getto all'asse di simmetria del venturi
        dgetto: diametro del getto
    
    Returns:
        coefficiente di attrito
    """
    reynolds_fuel = NumeroDiReynoldsBenzina(Tamb,pamb,deltap,d3,d2max,d2min,hc,hd,dgetto)
    
    if reynolds_fuel<=2500:
        lambda_fuel = 64/reynolds_fuel
    else:
        f_fuel = lambda lambda_fuel: 2*np.log10(reynolds_fuel*np.sqrt(lambda_fuel))-0.8-(1/             
        np.sqrt(lambda_fuel))
        D_f_fuel = lambda lambda_fuel: 1/(2*lambda_fuel**1.5)+1/(lambda_fuel*np.log(10))
        lambda_fuel = newton(f_fuel,D_f_fuel,0.0005)
    
    return lambda_fuel


def Coefficiente_efflusso_benzina(Tamb,pamb,deltap,d3,d2max,d2min,hc,hd,dgetto,lcd):
    lambdaB = coefficiente_attrito_benzina(Tamb,pamb,deltap,d3,d2max,d2min,hc,hd,dgetto)
    
    return 1/np.sqrt(1+((lambdaB*lcd)/(dgetto)))

def portata_benzina(Tamb,pamb,deltap,d3,d2max,d2min,hc,hd,dgetto,lcd):
    coeffBenz = Coefficiente_efflusso_benzina(Tamb,pamb,deltap,d3,d2max,d2min,hc,hd,dgetto,lcd)
    P2 = PressioneAriaTeorica2(Tamb,pamb,deltap,d3,d2max,d2min)
    RhoB = densitBenzina(Tamb)  
    areaGetto = areaSezioneGetto(dgetto)

    return areaGetto*coeffBenz*np.sqrt((2*RhoB*((pamb-P2)-RhoB*(Constants.g)*(hd-hc))))


######################### RAPPORTO ARIA BENZINA #####################################################

def rapporto_aria_benzina(Tamb, pamb, phi, deltap, d1, d3, d2max, d2min,hc,hd, dgetto, lcd, r_n0 = 1):
    """ 
    metodo di Newton implementato per la stima del coefficiente di attrito del getto 
    
    Args:
        Tamb: temperatura ambiente
        pamb: pressione ambiente
        deltap: pressione differenziale tra la pressione ambiente e la pressione nella sezione 3
        d3: diametro della sezione 3
        d2max: diametro massimo della sezione di gola
        d2min: diametro minimo della sezione di gola
        hc: altezza dal ingresso del getto al pelo libero della benzina nella vaschetta
        hd: altezza dall'uscita del getto all'asse di simmetria del venturi
        dgetto: diametro del getto
    
    Returns:
        coefficiente di attrito
    """
    portataA = portata_aria(Tamb, pamb, phi, deltap, d1, d3, d2max, d2min, r_n0 = 1)
    portataB = portata_benzina(Tamb,pamb,deltap,d3,d2max,d2min,hc,hd,dgetto,lcd)
        
    return portataA / portataB


def errore_rapporto_AF(Tamb, pamb, phi, deltap, d1, d3, d2max, d2min,hc,hd, dgetto, lcd):
    AF = rapporto_aria_benzina(Tamb, pamb, phi, deltap, d1, d3, d2max, d2min,hc,hd, dgetto, lcd)
    return np.abs((AF-14.7)/14.7)*100

def lable_mixture(Tamb, pamb, phi, deltap, d1, d3, d2max, d2min,hc,hd, dgetto, lcd):
    AF = rapporto_aria_benzina(Tamb, pamb, phi, deltap, d1, d3, d2max, d2min,hc,hd, dgetto, lcd)
    if AF < 14.6:
        mix = "Rich mixture"

    if AF >= 14.6 and AF <= 14.8:
        mix = "Stoichiometric mixture"

    if AF >= 14.8:
        mix = "Lean mixture"

    return mix