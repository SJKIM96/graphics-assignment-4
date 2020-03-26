class shader:

  def __shadowed(self,object,I,S,objectList):
	  #Complete this helper method
    epsonlon = 0.001
    M = object.getTinv().inverse()
    I = M*(I + S.scalarMultiply(epsonlon))
    S = M * S
    for obj in objectList:
      mInv = obj.getTinv()
      In = mInv* I
      Sn = mInv * S
      if (obj.intersection(In,Sn) != -1.0):
        return True
    return False

  def __init__(self,intersection,direction,camera,objectList,light):
    #Complete this method  
    obj = intersection[0]
    t0 = intersection[1]
    mInverse = obj.getTinv()
    Ts = mInverse * light.getPosition()
    Te = mInverse * camera.getE()
    Td = mInverse * direction
    I = Te + Td.scalarMultiply(t0)
    S = Ts - I
    S = S.normalize()
    N = obj.normalVector(I)
    R = -S + N.scalarMultiply(S.dotProduct(N) *2)
    V = Te - I
    V = V.normalize()
    Id = max(N.dotProduct(S),0)
    Is = max(R.dotProduct(V),0)
    
    r = obj.getReflectance()
    c= obj.getColor()
    Li= light.getIntensity()
    
    f = 0
    if(not self.__shadowed(obj,I,S,objectList)):
      f= r[0] + r[1] * Id + r[2]* Is ** r[3]
    else:
      f = r[0]
    
    self.__color = (int(c[0] * Li[0] *f), int(c[1] * Li[1] *f),int(c[2] * Li[2] *f))

  def getShade(self):
    return self.__color