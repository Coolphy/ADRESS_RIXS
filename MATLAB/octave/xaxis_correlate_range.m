function corrdata = xaxis_correlate_range(refdata,uncorrdata,range)
tempref = refdata(1,range(1):range(2));
tempdata = uncorrdata(1,range(1):range(2));

[r,lags] = xcorr(tempref,tempdata);
[m,p] = max(r);

corrdata = circshift(uncorrdata,lags(p));
end