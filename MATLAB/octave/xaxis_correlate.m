function corrdata = xaxis_correlate(refdata,uncorrdata)
[r,lags] = xcorr(refdata,uncorrdata);
[m,p] = max(r);
corrdata = circshift(uncorrdata,lags(p));
end