function data = load_rixs(run_array)
filenumber=length(run_array);
data=[];
for i=1:filenumber
runnumber = run_array(i);
data((i*3-2):(i*3),:)=load_ccd(runnumber);
if i == 1
data(2,:)=xaxis_correlate(data(1,:),data(2,:));
data(3,:)=xaxis_correlate(data(1,:),data(3,:));
else
data((i*3-2),:)=xaxis_correlate(data(1,:),data((i*3-2),:));
data((i*3-1),:)=xaxis_correlate(data(1,:),data((i*3-1),:));
data((i*3),:)=xaxis_correlate(data(1,:),data((i*3),:));
end
end
end