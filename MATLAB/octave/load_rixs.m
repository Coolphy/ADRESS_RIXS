function data = load_rixs(runs)
global path
filelist = []
for i = 1:length(runs)
  filename = make_name(runs(i));
  for i = 1:3
    filelist(i) = sprintf('%s_d%d.h5',filename,i);
  end
end
data = load_ccd(fileList,path)
end
end
