function ccd = load_ccd(runnumber)
global path
filename = make_name(runnumber);
ccd = [];
for i = 1:3
fullname = sprintf('%s/%s_d%d.h5',path,filename,i);
ccd(i,:) = load_h5(fullname);
end
end