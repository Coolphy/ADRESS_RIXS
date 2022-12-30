%%
pkg load signal;

global path
global base
global energy_dispersion
path = 'C:\Researches\Scripts\plotRIXS\test\';
base = 'Fe';
energy_dispersion = 0.004;


%%
data = load_rixs([25,26,27,28,29]);
for i = 1:size(data,1)
plot(data(i,:));
hold on;
end
hold off;


%%
data = correlate_rixs(data,[2410,2500]);
for i = 1:size(data,1)
plot(data(i,:));
hold on;
end
xlim([2410,2500])
hold off;


%%
sumdata = data(1,:);
for i = 2:size(data,1)
sumdata = sumdata + data(i,:);
end
plot(sumdata)


%%
[x,y] = zero_energy(sumdata,2451);
plot(x,y)




