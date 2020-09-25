# IOEDDY: input/output library for postprocessing of Eddy.f

import numpy as np

import matplotlib as ml
import matplotlib.pyplot as plt
import struct as st

#-------------------------------------------------------------


def readgrid(filename):

	f = open(filename)

	nx = int(f.read(4))

        #nx = np.fromfile(f, dtype=int, count=1)

	index,x=np.loadtxt(filename,skiprows=1,unpack=1)

	xe = np.zeros(nx+1)
	xc = np.zeros(nx+1)

	xe[:len(x)]=x[:]; xe[-1]=xe[-2] + (xe[-2]-xe[-3]); #only required for consistency of the allocation

	for ii in range(1, nx+1):

		xc[ii] = (xe[ii] + xe[ii-1]) * 0.5

	xc[0] = xe[0] - (xc[1]-xe[0]) 

	return  nx, index, x, xe, xc 

#-------------------------------------------------------------

def readres_old(filename):

	f = open(filename,'rb')

	header = np.dtype([('dummy1','int32'),('i','int32'),\
	('j','int32'),('k','int32'),('jp','int32'),\
	('dummy2','int32')])


	my_header = np.fromfile(f,header)

	i = my_header['i'][0]
	j = my_header['j'][0]
	k = my_header['k'][0]


	f.close()

	f= open(filename,'rb')

	raw_data=np.dtype([('dummy1i','int32'),\
	('data1','float64',(i*j,)),\
        ('dummy2i','int32')])

	restart = np.dtype([('dummy1','int32'),('i','int32'),\
	('j','int32'),('k','int32'),('jp','int32'),\
	('dummy2','int32'),('my_raw_data',raw_data,(100,)),('dummy3','int32'),('nstep','int32'),\
	('dummy4','int32'),('dummy5','int32'),('time','float64'),('dummy6','int32'),\
	('dummy7','int32'),('dtm1','float64'),('grav','float64'),('dummy8','int32')])


	my_restart = np.fromfile(f,restart)

	if my_restart['dummy7'][0] == my_restart['dummy8'][0]:
		print('Reading correct')

	else:   
		print('Reading error')
		print(my_restart['dummy1'][0],my_restart['dummy2'][0])
		print(my_restart['dummy3'][0],my_restart['dummy4'][0])
		print(my_restart['dummy5'][0],my_restart['dummy6'][0])
		print(my_restart['dummy7'][0],my_restart['dummy8'][0])

	f.close()



	my_raw_data = my_restart['my_raw_data'][0]


	data = np.zeros((i,j,k))

	for kk in range(0,k-1):

		data[:,:,kk]=np.reshape(my_raw_data[kk][1],(i,j),order='F')


	return my_restart,data


#-------------------------------------------------------------


def center(var,data,i,j,k):

# Center velocity
	if var == 'u':

		for ii in range(1,i-2): #ii 2 to i-1
			for jj in range(1,j-2):
				for kk in range (1,k-2):
	    
					data[ii,jj,kk] = 0.5 * (data[ii,jj,kk] + data[ii-1,jj,kk])	
	if var == 'v':

		for ii in range(1,i-2): #ii 2 to i-1
			for jj in range(1,j-2):
				for kk in range (1,k-2):
	    
					data[ii,jj,kk] = 0.5 * (data[ii,jj,kk] + data[ii,jj-1,kk])	
		


	if var == 'w':

		for ii in range(1,i-2): #ii 2 to i-1
			for jj in range(1,j-2):
				for kk in range (1,k-2):
	    
					data[ii,jj,kk] = 0.5 * (data[ii,jj,kk] + data[ii,jj,kk-1])	
			
     

	return data




#-------------------------------------------------------------


def readpln(filename):

	f = open(filename,'rb')

	header = np.dtype([('dummy1','int32'),('nstep','int32'),\
	('time','float64'),('dt','float64'),('g','float64'),\
	('dens_0','float64'),('Re','float64'),('Pr','float64'),\
	('dummy2','int32'),('dummy3','int32'),('norm','int32'),\
	('index','int32'),('iu','int32'),('iv','int32'),('iw','int32'),\
	('dummy4','int32'),('dummy5','int32'),('cloc','float64'),\
	('eloc','float64'),('dummy6','int32'),('dummy7','int32'),\
	('np1','int32'),('np2','int32'),\
	('dummy8','int32'),('dummy9','int32')])


	my_header = np.fromfile(f,header)

	np1 = my_header['np1'][0]
	np2 = my_header['np2'][0]

	f.close()

	f= open(filename,'rb')

	plane = np.dtype([('dummy1','int32'),('nstep','int32'),\
	('time','float64'),('dt','float64'),('g','float64'),\
	('dens_0','float64'),('Re','float64'),('Pr','float64'),\
	('dummy2','int32'),('dummy3','int32'),('norm','int32'),\
	('index','int32'),('iu','int32'),('iv','int32'),('iw','int32'),\
	('dummy4','int32'),('dummy5','int32'),('cloc','float64'),\
	('eloc','float64'),('dummy6','int32'),('dummy7','int32'),\
	('np1','int32'),('np2','int32'),\
	('dummy8','int32'),('dummy9','int32'),\
	('gc1','float64',(np1,)),('ge1','float64',(np1,)),\
	('dummy10','int32'),('dummy11','int32'),\
        ('gc2','float64',(np2,)),('ge2','float64',(np2,)),\
        ('dummy12','int32'),('dummy13','int32'),\
	('data','float32',(np1*np2,)),('dummy14','int32')])


	my_plane = np.fromfile(f,plane)
 
	if my_plane['dummy13'][0] == my_plane['dummy14'][0]:
		print('Reading correct')
	else:
		print('Reading error')
		print(my_plane['dummy1'][0],my_plane['dummy2'][0],my_plane['dummy3'][0])
		print(my_plane['dummy4'][0],my_plane['dummy5'][0],my_plane['dummy6'][0])
		print(my_plane['dummy7'][0],my_plane['dummy8'][0],my_plane['dummy9'][0])
		print(my_plane['dummy10'][0],my_plane['dummy11'][0],my_plane['dummy12'][0])
		print(my_plane['dummy13'][0],my_plane['dummy14'][0])

	f.close()

	return my_plane

#--------------------------------------------------------

def loc(v,a):
	i = (np.abs(a - v)).argmin()
	return i

#-------------------------------------------------------------

def figRange(a):
   
    if   a =='W':
        i =[-0.05,0.25]
    elif a =='V':
        i =[-0.001,0.001]
    elif a =='U':
        i =[-0.001,0.001]
    elif a =='omgx':
        i =[-0.0008,0.0008]  
    elif a =='omgt':
        i =[-0.001,0.001]      
    elif a =='omgz':
        i =[-0.001,0.001]  
    elif a =='P':
        i =[-0.01,0.01]
    elif a == 'RHO':
        i=[-0.001,0.001]
    else:
        print('Check input to figRange')

    return i
        
#-------------------------------------------------------------


def readres(filename):
#remember: f.seek(),f.tell()

	f = open(filename,'rb')

	_,i,j,k,jp,_ = st.unpack('i'*6,f.read(24))

	data=np.zeros([i,j,k],dtype=float)

	for kk in range (0,k):
	     	
		dummy1 = st.unpack('i',f.read(4))    
		data[:,:,kk]=np.reshape(st.unpack('d'*i*j,f.read(8*i*j)),(i,j),order='F')
		dummy2 = st.unpack('i',f.read(4))
	    
		if dummy1!=dummy2:
			print('Error reading',kk)
			break

	_,it,_,_,time,_,_,dt,grav,_=st.unpack('iiiidiiddi',f.read(4*7+3*8)) 


	return i,j,k,it,time,dt,grav,data

#-------------------------------------------------------------


def read5p(filename):
#remember: f.seek(),f.tell()

	f = open(filename,'rb')

	_,i,j,k,jp,_ = st.unpack('i'*6,f.read(24))

	data=np.zeros([i,j,k],dtype=float)

	for kk in range (0,k):
	     	
		dummy1 = st.unpack('i',f.read(4))    
		data[:,:,kk]=np.reshape(st.unpack('d'*i*j,f.read(8*i*j)),(i,j),order='F')
		dummy2 = st.unpack('i',f.read(4))
	    
		if dummy1!=dummy2:
			print('Error reading',kk)
			break

	_,it,_,_,time,_,_,dt,grav,_,_,kmin5p,kmax5p,nzg=st.unpack('iiiidiiddiiiii',f.read(4*11+3*8)) 


	return i,j,k,it,time,dt,grav,kmin5p,kmax5p,nzg,data


def nextpow2(i):
    n = 1
    while n < i: n *= 2
    return n