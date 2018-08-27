%%%matlab script for generating spider web geometry and lammps input file
%%%Wroten by Zhao Qin 2013 @MIT
%%%Please refer to Zhao Qin, Markus Buhler, Nature Materials, 2013
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%Double comments are personal notes- Zachar 2018
clear;
dd=0.00102; %default 0.00102 
dr=0.08; %default values 0.02 0.04 0.08, controlling the number of spiral threads
%%Distance between spiral threads. 0.1 = 10 units. 
%%Serves no purpose anymore, just as a fallback (which will change the code anyways so will probably be trashed.)

%nthread=8; %default 12
nthread = input('Number of radial threads: ');


%%nbead=1000; %%Web structure radius (10 = 1 units) 
nbead = input('What should the radius of the web structure be?: ');
nbead = nbead * 10;

netrange=99/100;
startspiral=20; 
datascale=1; %scale for the coordinates in the data file default 1
xyzfactor=100;
ifdroplet=0.0;   %probability to have water droplet; default 0.1
xlow=99999;
xhigh=-99999;
ylow=99999;
yhigh=-99999;
zlow=99999;
zhigh=-99999;
patom=1;
pdrop=1;
pbond=1;
pdropbond=1;
pangle=1;

for i=1:nthread
    r0=dd/(2*pi/nthread);
    
    sita0=(i-1)*2*pi/nthread;

    xcentra=r0*cos(sita0);
    ycentra=r0*sin(sita0);
    zcentra=0.0;
    xtemp=(r0+dd*(nbead-1))*cos(sita0);
    ytemp=(r0+dd*(nbead-1))*sin(sita0);
    ztemp=0.0;
    for j=1:nbead
        atom(patom,1)=xcentra+(xtemp-xcentra)/(nbead-1)*(j-1);   % x
        atom(patom,2)=ycentra+(ytemp-ycentra)/(nbead-1)*(j-1);   % y
        atom(patom,3)=zcentra+(ztemp-zcentra)/(nbead-1)*(j-1);   % z
        atom(patom,4)=i;  %molecule ID
        atom(patom,5)=patom; %atom IDalso 
        atom(patom,6)=1; %atom type
        if(atom(patom,1)>xhigh)
            xhigh=atom(patom,1);
        end
        if(atom(patom,1)<xlow)
            xlow=atom(patom,1);
        end    
        if(atom(patom,2)>yhigh)
            yhigh=atom(patom,2);
        end
        if(atom(patom,2)<ylow)
            ylow=atom(patom,2);
        end     
        if(atom(patom,3)>zhigh)
            zhigh=atom(patom,3);
        end
        if(atom(patom,3)<zlow)
            zlow=atom(patom,3);
        end           
        patom=patom+1;      
        if(ifdroplet>0)
            kkk=rand;
            if(kkk<ifdroplet)
                atomdrop(pdrop,1:3)=atom(patom-1,1:3);
                atomdrop(pdrop,3)=atomdrop(pdrop,3)-1.3*dd;
                atomdrop(pdrop,4)=nthread+2; %atom type
                atomdrop(pdrop,5)=pdrop; %atom ID
                atomdrop(pdrop,6)=3; %atom type
                pdrop=pdrop+1;
                bonddrop(pdropbond,1)=patom-1;
                bonddrop(pdropbond,2)=pdrop-1;
                bonddrop(pdropbond,3)=4;
                pdropbond=pdropbond+1;
            end
        end
        if(j~=1)
            bond(pbond,2)=patom-1;
            bond(pbond,1)=patom-2;
            bond(pbond,3)=1;
            pbond=pbond+1;
        elseif(j==1 && i>1)
            bond(pbond,2)=patom-1;
            bond(pbond,1)=patom-1-nbead;
            bond(pbond,3)=2;
            pbond=pbond+1;
            if(i==nthread)
                bond(pbond,2)=patom-1;
                bond(pbond,1)=1;
                bond(pbond,3)=2;
                pbond=pbond+1;
            end
        end 
        if(j>2)
            angle(pangle,1)=patom-3;
            angle(pangle,2)=patom-2;
            angle(pangle,3)=patom-1;
            angle(pangle,4)=1;
            pangle=pangle+1;
        end
    end
end

stoplength=dd*(nbead-1-startspiral)*netrange;
%%round=floor(stoplength/dr); %%Number of spiral threads
%%rincr=floor(dr/nthread/dd); 


round = input('Desired quantity of spiral threads: ');
if isempty(round)
    round=floor(stoplength/dr); %%Number of spiral threads
    roundDefault = ['Set to default: ', num2str(round)];
    disp(roundDefault);
end

rincr = input('Base distance between spiral threads: ');
if isempty(rincr)
    rincr=floor(dr/nthread/dd);
    rincrDefault = ['Set to default: ', num2str(rincr)];
    disp(rincrDefault);
end;

spiralSpacingType = input('Is the spiral thread spacing fixed, linear, or geometric? (Respond f, l, or g): ', 's');
while spiralSpacingType ~= 'f' & spiralSpacingType ~= 'g' & spiralSpacingType ~= 'l'
    disp(['Invalid input'])
    spiralSpacingType = input('Is the spiral thread spacing fixed, linear, or geometric? (Respond f, l, or g): ', 's');
end

if spiralSpacingType == 'l'
    spiralLinearConstant = input('Linear constant: ');

elseif spiralSpacingType == 'g'
    spiralGeometricConstant = input('Geometric constant: ');

%{
increment one at a time

%}

end;

r0=1+startspiral;

for i=1:round
    %%once each radial thread level
    if i ~= 1
        if spiralSpacingType == 'l'
            rincr = rincr + spiralLinearConstant;
        elseif spiralSpacingType == 'g'
            rincr = rincr * spiralGeometricConstant;
        end;
    end;
    for j=1:nthread
        sita0=(j-1)*2*pi/nthread;
        sita1=j*2*pi/nthread;
        %% Finds segment of circumference. First spiral height, then the next one.
        xcentra=r0*dd*cos(sita0);        
        ycentra=r0*dd*sin(sita0);
        zcentra=dd;
        xtemp=(r0+rincr)*dd*cos(sita1);
        ytemp=(r0+rincr)*dd*sin(sita1);
        ztemp=dd;
        nnb=floor((((xtemp-xcentra)^2+(ytemp-ycentra)^2+(ztemp-zcentra)^2)^0.5)/dd)+1;
        for k=1:nnb-1
            atom(patom,1)=xcentra+(xtemp-xcentra)/(nnb-1)*(k-1);   % x
            atom(patom,2)=ycentra+(ytemp-ycentra)/(nnb-1)*(k-1);   % y
            atom(patom,3)=zcentra+(ztemp-zcentra)/(nnb-1)*(k-1);   % z
            atom(patom,4)=nthread+1;  %molecule ID
            atom(patom,5)=patom; %atom ID
            atom(patom,6)=2; %atom type
        if(atom(patom,1)>xhigh)
            xhigh=atom(patom,1);
        end
        if(atom(patom,1)<xlow)
            xlow=atom(patom,1);
        end    
        if(atom(patom,2)>yhigh)
            yhigh=atom(patom,2);
        end
        if(atom(patom,2)<ylow)
            ylow=atom(patom,2);
        end     
        if(atom(patom,3)>zhigh)
            zhigh=atom(patom,3);
        end
        if(atom(patom,3)<zlow)
            zlow=atom(patom,3);
        end           
        patom=patom+1;
        if(ifdroplet>0)
            kkk=rand;
            if(kkk<ifdroplet)
                atomdrop(pdrop,1:3)=atom(patom-1,1:3);
                atomdrop(pdrop,3)=atomdrop(pdrop,3)-1.3*dd;
                atomdrop(pdrop,4)=nthread+2; %atom type
                atomdrop(pdrop,5)=pdrop; %atom ID
                atomdrop(pdrop,6)=3; %atom type
                pdrop=pdrop+1;
                bonddrop(pdropbond,1)=patom-1;
                bonddrop(pdropbond,2)=pdrop-1;
                bonddrop(pdropbond,3)=4;
                pdropbond=pdropbond+1;
            end
        end
        if(i==1 && j==1 && k==1)
        else
            bond(pbond,2)=patom-1;
            bond(pbond,1)=patom-2;
            bond(pbond,3)=3;
            pbond=pbond+1;
        end 
        if(k==1)
            bond(pbond,2)=patom-1;
            bond(pbond,1)=(j-1)*nbead+r0;
            bond(pbond,3)=2;
            pbond=pbond+1;
        end 
        if(i==1 && j==1 && k<3)
            i;
        else
            angle(pangle,1)=patom-3;
            angle(pangle,2)=patom-2;
            angle(pangle,3)=patom-1;
            angle(pangle,4)=2;
            pangle=pangle+1;
        end
        end
        r0=r0+rincr;
    end
end
atom(patom,1)=xcentra+(xtemp-xcentra)/(nnb-1)*(k);   % x
atom(patom,2)=ycentra+(ytemp-ycentra)/(nnb-1)*(k);   % y
atom(patom,3)=zcentra+(ztemp-zcentra)/(nnb-1)*(k);   % z
atom(patom,4)=nthread+1;  %molecule ID
atom(patom,5)=patom; %atom ID
atom(patom,6)=2; %atom type
patom=patom+1;
bond(pbond,2)=patom-1;
bond(pbond,1)=r0;
bond(pbond,3)=2;
pbond=pbond+1;
bond(pbond,2)=patom-1;
bond(pbond,1)=patom-2;
bond(pbond,3)=3;
pbond=pbond+1;
angle(pangle,1)=patom-3;
angle(pangle,2)=patom-2;
angle(pangle,3)=patom-1;
angle(pangle,4)=2;
pangle=pangle+1;

sizeatom=size(atom);
sizebond=size(bond);
sizeangle=size(angle);

if(ifdroplet>0)
sizedrop=size(atomdrop);
sizedropbond=size(bonddrop);
for i=1:sizedrop(1)
    atom(sizeatom(1)+i,1:6)=atomdrop(i,1:6);
    atom(sizeatom(1)+i,5)=atom(sizeatom(1)+i,5)+sizeatom(1);
end
for i=1:sizedropbond(1)
    bond(sizebond(1)+i,1:3)=bonddrop(i,1:3);
    bond(sizebond(1)+i,2)=bond(sizebond(1)+i,2)+sizeatom(1);
end
sizeatom=size(atom);
sizebond=size(bond);
end

%%%output of the oringinal network model%%%%%%%%%%%%%%%55
outputname=['matlab.data'];
outputnamexyz=['matlab.xyz'];

fidw=fopen(outputname,'w');
fidwxyz=fopen(outputnamexyz,'w');
fprintf(fidw,'LAMMPS data file written by pdb2lammps_ice.m\n');
fprintf(fidw,'%10d    atoms\n',sizeatom(1));
fprintf(fidw,'%10d    bonds\n',sizebond(1));
fprintf(fidw,'%10d    angles\n',sizeangle(1));
fprintf(fidw,'%10d    dihedrals\n',0);
fprintf(fidw,'%10d    impropers\n',0);
if(ifdroplet>0)
fprintf(fidw,'%10d    atom types\n',3);
fprintf(fidw,'%10d    bond types\n',4);
else
fprintf(fidw,'%10d    atom types\n',2);
fprintf(fidw,'%10d    bond types\n',3);
end
fprintf(fidw,'%10d    angle types\n',2);
fprintf(fidw,'%10d    dihedral types\n',0);
fprintf(fidw,'%10d    improper types\n',0);
fprintf(fidw,'\n');
fprintf(fidw,'%f %f   xlo xhi\n',xlow-0.5*(xhigh-xlow),xhigh+0.5*(xhigh-xlow));
fprintf(fidw,'%f %f   ylo yhi\n',ylow-0.5*(yhigh-ylow),yhigh+0.5*(yhigh-ylow));
fprintf(fidw,'%f %f   zlo zhi\n',zlow-10*(zhigh-zlow)-1,zhigh+10*(zhigh-zlow)+1);
fprintf(fidw,'\n');
fprintf(fidw,'Masses\n');
fprintf(fidw,'\n');
if(ifdroplet>0)
fprintf(fidw,'   %d  1.577e-11\n',1);
fprintf(fidw,'   %d  5.88e-12\n',2);
fprintf(fidw,'   %d  1e-4\n',3);
else
fprintf(fidw,'   %d  1.577e-11\n',1);
fprintf(fidw,'   %d  5.88e-12\n',2);
end
fprintf(fidw,'\n');
fprintf(fidw,'Atoms\n');
fprintf(fidw,'\n');
for i=1:sizeatom(1)
    fprintf(fidw,'   %d   %d   %d   %f   %f   %f\n',atom(i,5),atom(i,4),atom(i,6),atom(i,1)*datascale,atom(i,2)*datascale,atom(i,3)*datascale);
end
fprintf(fidw,'\n');
fprintf(fidw,'Bonds\n');
fprintf(fidw,'\n');
for i=1:sizebond(1)
    fprintf(fidw,'     %d     %d     %d     %d\n',i,bond(i,3),bond(i,1),bond(i,2));
end
fprintf(fidw,'\n');
fprintf(fidw,'Angles\n');
fprintf(fidw,'\n');
for i=1:sizeangle(1)
    fprintf(fidw,'     %d     %d     %d     %d     %d\n',i,angle(i,4),angle(i,1),angle(i,2),angle(i,3));
end
fprintf(fidwxyz,'%d \n',sizeatom(1));
fprintf(fidwxyz,'Atoms \n');
for i=1:sizeatom(1)
    fprintf(fidwxyz,'%d   %f   %f   %f\n',atom(i,6),atom(i,1)*xyzfactor,atom(i,2)*xyzfactor,atom(i,3)*xyzfactor);
end
fclose(fidw);
fclose(fidwxyz);