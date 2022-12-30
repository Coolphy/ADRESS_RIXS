function [xdata,sumdata] = load_runs(run_array)
filenumber=length(run_array);
for i=1:filenumber
runnumber = run_array(i);
if i == 1
[xdata,refdata]=load_rixs(runnumber);
sumdata=refdata;
else
[xdata,uncorrdata]=load_rixs(runnumber);
corrdata=xaxis_correlate(refdata,uncorrdata);
sumdata=sumdata+corrdata;
end
end
sumdata=sumdata/filenumber;
end