function data = load_rixs(runs)
global path
filelist=string();
for i = 1:length(runs)
  filename = make_name(runs(i));
  for j = 1:3
    filelist(i*3-3+j) = sprintf('%s_d%d.h5',filename,j);
  end
end
data = load_ccd(filelist,path);
end