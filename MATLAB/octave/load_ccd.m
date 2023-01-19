function data = load_ccd(filelist,dirname)
global data_dict;
filenumber=length(filelist);
data=[];
for i=1:filenumber
filename = filelist{i};
if ~isfield(data_dict,filename)
data_dict(1).(filename).ccd = load_h5([dirname,'/',filename]);
data(i,:)= data_dict(1).(filename).ccd;
else
data(i,:)= data_dict(1).(filename).ccd;
end
end
end
