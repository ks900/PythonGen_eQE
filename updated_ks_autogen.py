#!/usr/bin/env python

# Khurshid Sohail

import sys
import shutil
import fileinput
import os
from os import walk 
import string
import subprocess
import time
import errno
import imp
from itertools import chain
import argparse
#from argsparse import ArugmentParser, REMAINDER 
from os.path import expanduser

newlist=[]
monlist=[]
tmp_array=[]
defaults=['H', 'C', 'O', 'N']

def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("--directory", "-d", action="store", help="directory which will store new files");
        parser.add_argument("--spath", "-p", action="store", help="full path to directory")
        parser.add_argument("--fde", "-f", action="store", help="the types of charges we want")
        args=parser.parse_args()
        global superpath
        global maindir
        if args.directory:
                if args.spath:
			if args.fde:
				superpath=args.spath
				maindir=args.directory
				frag=args.fde
				traverse(superpath, maindir, frag)

def traverse(superpath, maindir, frag):
	pathx="monomer-a/"
        pathbx="monomer-b/"
        dim0_pathx="dimer.scf_0.in"
        dim1_pathx="dimer.scf_1.in"
        zx="PBE0/"
        ox="PBE1/"
        fx="PBE.5"
	zero=["zero"]
        one=["one"]
        five=["five"]
        zo=["zero", "one"]
        zf=["zero", "five"]
        of=["one", "five"]
        zfo=["zero","five", "one"]
	path=os.path.join(superpath,pathx)
        pathb=os.path.join(superpath,pathbx)
        dst_p=os.path.join(superpath, maindir)
        dim0_path=os.path.join(superpath, dim0_pathx)
        dim1_path=os.path.join(superpath, dim1_pathx)
        os.mkdir(dst_p, 0755)
        z=os.path.join(dst_p, zx)
        o=os.path.join(dst_p, ox)
        f=os.path.join(dst_p, fx)
        if frag=="zero":
                fr=zero
        if frag=="one":
                fr=one
        if frag=="five":
                fr=five
        if frag=="zo":
                fr=zo
        if frag=="zf":
                fr=zf
        if frag=="of":
                fr=of
        if frag=="zfo":
                fr=zfo
	

	filenames = os.listdir(path)
	filenames.sort()
	mon_a=filenames
	mon_b=os.listdir(pathb)
	for files in filenames:
		newlist.append(files.strip('.xyz'))
		os.mkdir(os.path.join(dst_p,files.strip('.xyz')), 0755 )
	newlist.sort()
	for aa in fr:
		for i in filenames:
			a=0
			txt=open(os.path.join(path, i), 'r')
			lines=txt.readlines()
			make=0
			cnt=0
			tmp=newlist[a]
			a+=1
					
			with open('dimer.scf_0.out') as template:
			    with  open('dimer.scf_0.in','w') as outfile:
				 for line in template:
					if 'nat =' in line:
						line = '    nat = '+str(lines[0])
					if 'ntyp =' in line:
						for x in lines:
							for check in defaults:
								if check in tmp_array:
									make+=1	
								elif check in x:
									
									tmp_array.append(check)
									cnt+=1
									line = '    ntyp = '+str(cnt)+'\n';
							
							
					if 'ATOMIC_SPECIES' in line:
						line='ATOMIC_SPECIES\n'
						for spec in tmp_array:
							line+=''
							
							if spec == "H":
								line+= 'H   1.00790    h_pbe_v1.4.uspp.F.UPF\n'
							elif spec ==  "N":
								line+= 'N   14.0067    n_pbe_v1.2.uspp.F.UPF\n'
							elif spec == "O":
								line+= 'O   15.9994    o_pbe_v1.2.uspp.F.UPF\n'
							elif spec == "C":
								line+= 'C   12.0107    c_pbe_v1.2.uspp.F.UPF\n'					
					if 'ATOMIC_POSITIONS angstrom' in line:
						line='ATOMIC_POSITIONS angstrom\n'
						for x in lines:
							line+=''
							if "H" in x:
								line+=x
							elif "C" in x:
								line+=x
							elif "O" in x:
								line+=x
							elif "N" in x:
								line+=x			
					if 'fde_frag_charge =' in line:
						if aa=="zero":
							line='    fde_frag_charge = 0.0\n'
						if aa=="one":
							line='    fde_frag_charge = 1.0\n'
						if aa=="five":
							line='    fde_frag_charge = 0.5\n'

								
					
					outfile.write(line)
			    del lines[:]
			    del tmp_array[:] 
			    dpi=os.path.join(dst_p,i.strip('.xyz'),aa)
			    os.mkdir(dpi, 0755)
			    shutil.copy(dim0_path, dpi)
	for aa in fr:
		for i in filenames:
			a=0
			txt=open(os.path.join(pathb, i), 'r')
			lines=txt.readlines()
			make=0
			cnt=0
			tmp=newlist[a]
			a+=1

			with open('dimer.scf_1.out') as template:
			    with  open('dimer.scf_1.in','w') as outfile:
				 for line in template:
					if 'nat =' in line:
						line = '    nat = '+str(lines[0])
					if 'ntyp =' in line:
						for x in lines:
							for check in defaults:
								if check in tmp_array:
									make+=1
								elif check in x:

									tmp_array.append(check)
									cnt+=1
									line = '    ntyp = '+str(cnt)+'\n';

					if 'ATOMIC_SPECIES' in line:
						line='ATOMIC_SPECIES\n'
						for spec in tmp_array:
							line+=''

							if spec == "H":
								line+= 'H   1.00790    h_pbe_v1.4.uspp.F.UPF\n'
							elif spec ==  "N":
								line+= 'N   14.0067    n_pbe_v1.2.uspp.F.UPF\n'
							elif spec == "O":
								line+= 'O   15.9994    o_pbe_v1.2.uspp.F.UPF\n'
							elif spec == "C":
								line+= 'C   12.0107    c_pbe_v1.2.uspp.F.UPF\n'
					if 'ATOMIC_POSITIONS angstrom' in line:
						line='ATOMIC_POSITIONS angstrom\n'
						for x in lines:
							line+=''
							if "H" in x:
								line+=x
							elif "C" in x:
								line+=x
							elif "O" in x:
								line+=x
							elif "N" in x:
								line+=x

					if 'fde_frag_charge =' in line:
						if aa=="zero":
							line='    fde_frag_charge = 1.0\n'
						if aa=="one":
							line='    fde_frag_charge = 0.0\n'
						if aa=="five":
							line='    fde_frag_charge = 0.5\n'


       		                        outfile.write(line)

                    	del lines[:]
                   	del tmp_array[:]
		    	dpi=os.path.join(dst_p,i.strip('.xyz'),aa)
                    	shutil.copy(dim1_path, dpi)



main()
