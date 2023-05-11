function [x,y] = plot_rixs(filePath,baseAtom,runList)

[x,y] = load_runs(filePath,baseAtom,runList);
figure();
plot(x,y);

end

function ccd = load_h5(filename)

ccd=h5read(filename,'/entry/analysis/spectrum');

end


function corrdata = correlatedata(refdata,uncorrdata)
[r,lags] = xcorr(refdata,uncorrdata);
[m,p] = max(r);
corrdata = circshift(uncorrdata,lags(p));
end


function fileName = make_name(baseAtom,runNo)

fileName = sprintf('%s_%04d',baseAtom,runNo);

end


function ccd = load_ccd(filePath,baseAtom,runNo)

global rixs_struct
fileName = make_name(baseAtom,runNo);
ccd = [];
if ~isfield(rixs_struct,fileName)
for i = 1:3
fullname = sprintf('%s/%s_d%d.h5',filePath,fileName,i);
ccd(i,:) = load_h5(fullname);
end
rixs_struct(1).(fileName) = ccd;
else
for i = 1:3
ccd = rixs_struct(1).(fileName);
end
end
end


function data = load_rixs(filePath,baseAtom,runNo)
ccd = load_ccd(filePath,baseAtom,runNo);
ccd(1,:) = correlatedata(ccd(2,:),ccd(1,:));
ccd(3,:) = correlatedata(ccd(2,:),ccd(3,:));
data = ccd(1,:)+ccd(2,:)+ccd(3,:);
end

function [xdata,sumdata] = load_runs(filePath,baseAtom,runList)
filenumber=size(runList,2);
for i=1:filenumber
runNo = runList(i);
if i == 1
refdata=load_rixs(filePath,baseAtom,runNo);
sumdata=refdata;
else
uncorrdata=load_rixs(filePath,baseAtom,runNo);
corrdata=correlatedata(refdata,uncorrdata);
sumdata=sumdata+corrdata;
end
end
xdata = [1:1:size(sumdata,2)];
end

