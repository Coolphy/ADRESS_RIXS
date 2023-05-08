function filename = make_name(runnumber)
global base;
filename = sprintf('%s_%04d',base,runnumber);
end