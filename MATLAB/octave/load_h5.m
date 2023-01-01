function ccd = load_h5(filename)

try
    f=load(filename);
    ccd = f.entry.analysis.spectrum;
catch
    ccd=h5read(filename,'/entry/analysis/spectrum');
end

end