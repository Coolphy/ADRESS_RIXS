function filelist = make_list(atom,start,last)
filelist = {};
j = 1;
for i = str2num(start):str2num(last)
    filelist{j} = sprintf('%s_%04d',atom,i);
    j=j+1;
end
end