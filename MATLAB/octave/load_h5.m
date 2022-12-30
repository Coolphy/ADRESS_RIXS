function ccd = load_h5(filename)
f=load(filename);
ccd = f.entry.analysis.spectrum;
end