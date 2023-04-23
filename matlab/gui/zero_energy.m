function [energydata,sumdata] = zero_energy(sumdata,zeropixel)
global energy_dispersion;
pixeldata = [1:1:length(sumdata)];
energydata = (pixeldata - zeropixel) .* energy_dispersion;
end