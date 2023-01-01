function data = load_ccd(filelist,dirname)
filenumber=length(filelist);
data=[];
for i=1:filenumber
filename = filelist{i};
data(i,:)=load_h5([dirname,'/',filename]);
end
end
