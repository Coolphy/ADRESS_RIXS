function [xdata,data] = load_rixs(runnumber)
ccd = load_ccd(runnumber);
ccd(1,:) = xaxis_correlate(ccd(2,:),ccd(1,:));
ccd(3,:) = xaxis_correlate(ccd(2,:),ccd(3,:));
data = (ccd(1,:)+ccd(2,:)+ccd(3,:))/3;
xdata = [1:1:length(data)];
end