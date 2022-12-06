
%%%%%%%%%%%%%%%%%
global path
global base
global energy_dispersion
path = 'C:/';
base = 'Fe';
energy_dispersion = 0.004;
exist rixs_struct;
if ~ans
global rixs_struct
rixs_struct = struct([]);
end
%%%%%%%%%%%%%%%%

[x,y] = load_runs([1:1:20])

%%%%%%%%%%%%%%%
function ccd = load_h5(filename)
% ccd=h5read(filename,'/entry/analysis/spectrum');
ccd = [1,2,3,4,5]
end

function filename = make_name(runnumber)
global base
filename = sprintf('%s_%04d',base,runnumber);
end

function ccd = load_ccd(runnumber)
global rixs_struct
global path
filename = make_name(runnumber);
ccd = [];
if ~isfield(rixs_struct,filename)
for i = 1:3
fullname = sprintf('%s/%s_d%d.h5',path,filename,i);
ccd(i,:) = load_h5(fullname);
end
rixs_struct(1).(filename).ccd = ccd;
else
for i = 1:3
ccd = rixs_struct(1).(filename).ccd;
end
end
end

function corrdata = correlatedata(refdata,uncorrdata)
[r,lags] = xcorr(refdata,uncorrdata);
[m,p] = max(r);
corrdata = circshift(uncorrdata,lags(p));
end

function energydata = zeroenergy(pixeldata,tempdata)
global energy_dispersion;
[pks,locs,w,p] = findpeaks(tempdata,'MinPeakHeight',max(tempdata)/20,'MinPeakProminence',3,'MinPeakWidth',4);
zeropixel = locs(size(locs,1));
energydata = (pixeldata - zeropixel) .* energy_dispersion;
end

function data = load_rixs(runnumber)
ccd = load_ccd(runnumber);
ccd(1,:) = correlatedata(ccd(2,:),ccd(1,:));
ccd(3,:) = correlatedata(ccd(2,:),ccd(3,:));
data = ccd(1,:)+ccd(2,:)+ccd(3,:);
end

function [xdata,sumdata] = load_runs(run_array)
filenumber=size(run_array,2);
for i=1:filenumber
runnumber = run_array(i);
if i == 1
refdata=load_rixs(runnumber);
sumdata=refdata;
else
uncorrdata=load_rixs(runnumber);
corrdata=correlatedata(refdata,uncorrdata);
sumdata=sumdata+corrdata;
end
end
xdata = [1:1:size(sumdata,2)];
end

