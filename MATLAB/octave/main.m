clf;
pkg load signal;

global path
global base
global energy_dispersion
path = 'C:\Researches\Scripts\plotRIXS\test\';
base = 'Fe';
energy_dispersion = 0.004;

[x,y] = load_runs([27,28,29]);
plot(x,y);

%plot(zero_energy(x,2046),y)