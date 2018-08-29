%%%matlab script for generating spider web geometry and lammps input file
%%%Writen by Zhao Qin 2013 @MIT
%%Modified by Zachar Hankewycz 2018 @MIT
%%(Double comments are 2018)
clear;

dd=1; %Scale factor- do not use, use datascale or xyzfactor instead.
spiralZfactor = 1;

%Radial thread quantity
radialQuantity = input('Number of radial threads: ');
while isempty(radialQuantity) || radialQuantity <= 2
    disp(['Invalid input'])
    radialQuantity = input('Number of radial threads: ');
end

%Radius of the web structure
webRadius = input('What should the radius of the web structure be?: ');
while isempty(webRadius) || webRadius < 1
    disp(['Invalid input'])
    webRadius = input('What should the radius of the web structure be?: ');
end
webRadius = webRadius * 10; %%(10 = 1 unit)


%%Scale factors- both should be used to scale models up/down. Each one only works for one file, has no cross-effect
datascale=1; %Scale factor of the coordinates in the .data file
xyzfactor=.1; %Scale factor of coordinates in .xyz file

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

%Creates radial threads
for i=1:radialQuantity
    r0=dd/(2*pi/radialQuantity);
    sita0=(i-1)*2*pi/radialQuantity;
    xcentra=r0*cos(sita0);
    ycentra=r0*sin(sita0);
    zcentra=0.0;
    xtemp=(r0+dd*(webRadius-1))*cos(sita0);
    ytemp=(r0+dd*(webRadius-1))*sin(sita0);
    ztemp=0.0;
    for j=1:webRadius
        atom(patom,1)=xcentra+((xtemp-xcentra)/(webRadius-1))*(j-1);   % x
        atom(patom,2)=ycentra+(ytemp-ycentra)/(webRadius-1)*(j-1);   % y
        atom(patom,3)=zcentra+(ztemp-zcentra)/(webRadius-1)*(j-1);   % z
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
        if(j~=1)
            bond(pbond,2)=patom-1;
            bond(pbond,1)=patom-2;
            bond(pbond,3)=1;
            pbond=pbond+1;
        elseif(j==1 && i>1)
            bond(pbond,2)=patom-1;
            bond(pbond,1)=patom-1-webRadius;
            bond(pbond,3)=2;
            pbond=pbond+1;
            if(i==radialQuantity)
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

round = input('Desired quantity of spiral threads: ');
while isempty(round)
    disp(["Invalid input. Please try again"]);
    round = input('Desired quantity of spiral threads: ');
end

rincr = input('Base distance between spiral threads: ');
while isempty(rincr)
    disp(["Invalid input. Please try again"]);
    rincr = input('Base distance between spiral threads: ');
end

spiralSpacingType = input('Is the spiral thread spacing fixed, linear, or geometric? (Respond f, l, or g): ', 's');
while spiralSpacingType ~= 'f' & spiralSpacingType ~= 'g' & spiralSpacingType ~= 'l'
    disp(['Invalid input'])
    spiralSpacingType = input('Is the spiral thread spacing fixed, linear, or geometric? (Respond f, l, or g): ', 's');
end

%%Null isn't not equal to those 3 values- maybe a type mismatch? Not sure, so I'm just going to check isempty() as well

while isempty(spiralSpacingType)
    disp(['Invalid input'])
    spiralSpacingType = input('Is the spiral thread spacing fixed, linear, or geometric? (Respond f, l, or g): ', 's');
end

if spiralSpacingType == 'l'
    spiralLinearConstant = input('Linear constant: ');

elseif spiralSpacingType == 'g'
    spiralGeometricConstant = input('Geometric constant: ');
end

r0=1+rincr*10; 
for i=1:round
    %%once each radial thread level
    if i ~= 1
        if spiralSpacingType == 'l'
            rincr = rincr + spiralLinearConstant;
        elseif spiralSpacingType == 'g'
            rincr = rincr * spiralGeometricConstant;
        end
    end
    for j=1:radialQuantity
        sita0=(j-1)*2*pi/radialQuantity;
        sita1=j*2*pi/radialQuantity;        
        xcentra=r0*dd*cos(sita0);        
        ycentra=r0*dd*sin(sita0);
        zcentra=spiralZfactor;
        xtemp=(r0+rincr)*dd*cos(sita1);
        ytemp=(r0+rincr)*dd*sin(sita1);
        ztemp=spiralZfactor;
        nnb=floor((((xtemp-xcentra)^2+(ytemp-ycentra)^2+(ztemp-zcentra)^2)^0.5)/dd)+1;
        for k=1:nnb-1
            atom(patom,1)=xcentra+(xtemp-xcentra)/(nnb-1)*(k-1);   % x
            atom(patom,2)=ycentra+(ytemp-ycentra)/(nnb-1)*(k-1);   % y
            atom(patom,3)=zcentra+(ztemp-zcentra)/(nnb-1)*(k-1);   % z
            atom(patom,4)=radialQuantity+1;  %molecule ID
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
        if(i==1 && j==1 && k==1)
        else
            bond(pbond,2)=patom-1;
            bond(pbond,1)=patom-2;
            bond(pbond,3)=3;
            pbond=pbond+1;
        end 
        if(k==1)
            bond(pbond,2)=patom-1;
            bond(pbond,1)=(j-1)*webRadius+r0;
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
atom(patom,4)=radialQuantity+1;  %molecule ID
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




%% Output

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
fprintf(fidw,'%10d    atom types\n',2);
fprintf(fidw,'%10d    bond types\n',3);
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
fprintf(fidw,'   %d  1.577e-11\n',1);
fprintf(fidw,'   %d  5.88e-12\n',2);
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

%%XYZ output
fprintf(fidwxyz,'%d \n',sizeatom(1));
for i=1:sizeatom(1)
    fprintf(fidwxyz,'%d   %f   %f   %f\n',atom(i,6),atom(i,1)*xyzfactor,atom(i,2)*xyzfactor,atom(i,3)*xyzfactor);
end
fclose(fidw);
fclose(fidwxyz);