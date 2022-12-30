function energydata = zero_energy(pixeldata,zeropixel)
global energy_dispersion;
energydata = (pixeldata - zeropixel) .* energy_dispersion;
end