function data = load_ccd(filelist,dirname)
global data_dict;
filenumber=length(filelist);
data=[];
for i=1:filenumber
filename = filelist{i};
if ~isfield(data_dict,filename(1:end-3))
data_dict(1).(filename(1:end-3)).ccd = load_h5([dirname,'/',filename]);
data(i,:)= data_dict(1).(filename(1:end-3)).ccd;
else
data(i,:)= data_dict(1).(filename(1:end-3)).ccd;
end
end
end
