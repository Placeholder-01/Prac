#!/usr/bin/env python

import sys
import datetime
import numpy as np
from scipy.sparse import coo_matrix
  
def make_dictionary(c):

  fn = ["/srv/gsfs0/projects/snyder/hayanlee/projects/FAP/pipeline/04_moabs/chr/JP/JP.G." + c + ".bed", "/srv/gsfs0/projects/snyder/hayanlee/projects/FAP/pipeline/04_moabs/chr/JP9/JP9.G." + c + ".bed", "/srv/gsfs0/projects/snyder/hayanlee/projects/FAP/pipeline/04_moabs/chr/JP6B/JP6B.G." + c + ".bed", "/srv/gsfs0/projects/snyder/hayanlee/projects/FAP/pipeline/04_moabs/chr/JPAdenoCa/JPAdenoCa.G." + c + ".bed"]
 
  dat = []
  row = []
  col = []
  for i in range(0, 4):
    print >> sys.stderr,"before f" + str(i), datetime.datetime.now()
    pos = []
    met = []
    with open(fn[i]) as lines:
      for l in lines:
        if l.startswith('#'):
          pass
        else:
          ele = l.strip().split()
          pos.append(int(ele[1]))
          met.append(float(ele[3]))
      dat += met
      col += pos
      row += [i]*len(met)

  F = coo_matrix((dat, (row, col))).tocsr()
  F1 = F.toarray()
  F1 [F1==0] = 0.0005
  M = np.zeros((F1.shape[0]-1, F1.shape[1]))
  M[0] = (F1[0,:] + F1[1,:])/2
  M[1] = (F1[0,:] + F1[2,:])/2
  M[2] = (F1[0,:] + F1[3,:])/2
  nonzero_pos = np.array(sorted(set(F.nonzero()[1])))
  print >> sys.stderr,"before return", datetime.datetime.now()
  return F1, M, nonzero_pos

def compute(c, l, sh):
  r = make_dictionary(c)

  for i in range(min(r[2]), max(r[2])-l+1, sh):
    idx = r[2][(i<r[2])&(r[2]<i+l)]
    F = r[0][:,idx]
    M = r[1][:,idx]
    #print >> sys.stderr, F, F.nonzero()
    jsd1 = np.sum((F[0,:]*np.log(F[0,:]/M[0,:])+F[1,:]*np.log(F[1,:]/M[0,:]))/2)
    jsd2 = np.sum((F[0,:]*np.log(F[0,:]/M[1,:])+F[2,:]*np.log(F[2,:]/M[1,:]))/2)
    jsd3 = np.sum((F[0,:]*np.log(F[0,:]/M[2,:])+F[3,:]*np.log(F[3,:]/M[2,:]))/2)

    print >> sys.stderr, "{}:{}-{}\t{:.2f}\t{:.2f}\t{:.2f}".format( c, i, i+l, jsd1, jsd2, jsd3 )
  return

def main():
  chrNumber = sys.argv[1]
  length = int(sys.argv[2])
  shift = int(sys.argv[3])
  #print("here")
  compute(chrNumber, length, shift)

if __name__ == "__main__":
    main()



