function corrdata = xaxis_correlate(refdata,uncorrdata)
try
pkg load signal;
end
[r,lags] = xcorr(refdata,uncorrdata);
[m,p] = max(r);
corrdata = circshift(uncorrdata,lags(p));
end