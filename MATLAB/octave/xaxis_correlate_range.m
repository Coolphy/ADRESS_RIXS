
function corrdata = xaxis_correlate_range(refdata,uncorrdata,range)

xdata = [1:length(refdata)];
tempref = refdata(find(xdata>range(1)&xdata<range(2)));
tempdata = uncorrdata(find(xdata>range(1)&xdata<range(2)));
try
pkg load signal;
end
[r,lags] = xcorr(tempref,tempdata);
[m,p] = max(r);

corrdata = circshift(uncorrdata,lags(p));
end
