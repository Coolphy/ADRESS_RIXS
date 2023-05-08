function data = correlate_rixs(data,range)
for i = 2:size(data,1)
data(i,:)=xaxis_correlate_range(data(1,:),data(i,:),range);
end
end