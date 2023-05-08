function info = load_h5(filename)

info = struct([]);
try
    f = load(filename);
    info(1).('ee') = sprintf('%.3f',mean(f.entry.instrument.NDAttributes.PhotonEnergy));
    p = mean(f.entry.instrument.NDAttributes.PolarMode);
    info(1).('tt') = sprintf('%.1f',mean(f.entry.instrument.NDAttributes.SampleTemp));
    info(1).('xx') = sprintf('%.3f',mean(f.entry.instrument.NDAttributes.SampleXs));
    info(1).('yy') = sprintf('%.3f',mean(f.entry.instrument.NDAttributes.SampleYs));
    info(1).('zz') = sprintf('%.3f',mean(f.entry.instrument.NDAttributes.SampleZ));
    info(1).('thth') = sprintf('%.3f',mean(f.entry.instrument.NDAttributes.SampleTheta));
    info(1).('phph') = sprintf('%.3f',mean(f.entry.instrument.NDAttributes.SamplePhi));
    info(1).('tltl') = sprintf('%.3f',mean(f.entry.instrument.NDAttributes.SampleTilt));
    info(1).('atat') = sprintf('%d',mean(f.entry.instrument.NDAttributes.AcquireTime));
    info(1).('spsp') = sprintf('%d',(f.entry.instrument.NDAttributes.ExposureSplit));
    info(1).('slsl') = sprintf('%.1f',mean(f.entry.instrument.NDAttributes.ExitSlit));
    info(1).('bcbc') = sprintf('%.0f',mean(f.entry.instrument.NDAttributes.BeamCurrent));
    
    
catch
    info(1).('ee')=sprintf('%.3f',mean(h5read(filename,'/entry/instrument/NDAttributes/PhotonEnergy')));
    p=mean(h5read(filename,'/entry/instrument/NDAttributes/PolarMode'));
    info(1).('tt')=sprintf('%.1f',mean(h5read(filename,'/entry/instrument/NDAttributes/SampleTemp')));
    info(1).('xx')=sprintf('%.3f',mean(h5read(filename,'/entry/instrument/NDAttributes/SampleXs')));
    info(1).('yy')=sprintf('%.3f',mean(h5read(filename,'/entry/instrument/NDAttributes/SampleYs')));
    info(1).('zz')=sprintf('%.3f',mean(h5read(filename,'/entry/instrument/NDAttributes/SampleZ')));
    info(1).('thth')=sprintf('%.3f',mean(h5read(filename,'/entry/instrument/NDAttributes/SampleTheta')));
    info(1).('phph')=sprintf('%.3f',mean(h5read(filename,'/entry/instrument/NDAttributes/SamplePhi')));
    info(1).('tltl')=sprintf('%.3f',mean(h5read(filename,'/entry/instrument/NDAttributes/SampleTilt')));
    info(1).('atat')=sprintf('%d',mean(h5read(filename,'/entry/instrument/NDAttributes/AcquireTime')));
    info(1).('spsp')=sprintf('%d',mean(h5read(filename,'/entry/instrument/NDAttributes/ExposureSplit')));
    info(1).('slsl')=sprintf('%.1f',mean(h5read(filename,'/entry/instrument/NDAttributes/ExitSlit')));
    info(1).('bcbc')=sprintf('%.0f',mean(h5read(filename,'/entry/instrument/NDAttributes/BeamCurrent')));
end

if p == 0
    info(1).('pp') = 'LH';
elseif p == 1
    info(1).('pp') = 'LV';
elseif p == 2
    info(1).('pp') = 'C+';
else
    info(1).('pp') = 'C-';
end

end