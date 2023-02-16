%%
addpath("/sls/X03MA/Data1/x03maop/RIXS/Wei_e20799/FePS3_Feb_2023/");
global rixs_struct
rixs_struct = struct([]);

%%
[x,y,d1,d2] = plot_mda_2d("/sls/X03MA/Data1/x03maop/RIXS/Wei_e20799/FePS3_Feb_2023/MDA/",13);
caxis([-0.2 -0.1]);

%%
[x,y,d1,d2] = plot_mda_2d("/sls/X03MA/Data1/x03maop/RIXS/Wei_e20799/FePS3_Feb_2023/MDA/",20);
% caxis([-0.2 -0.1]);

%%
[x,y,d1,d2] = plot_mda_2d("/sls/X03MA/Data1/x03maop/RIXS/Wei_e20799/FePS3_Feb_2023/MDA/",22);
caxis([-0.275 -0.25]);

%%
[en,tey,tfy] = plot_xas("/sls/X03MA/Data1/x03maop/RIXS/Wei_e20799/FePS3_Feb_2023/XAS/","Fe",18);

%%
[x,y] = plot_rixs("/sls/X03MA/Data1/x03maop/RIXS/Wei_e20799/FePS3_Feb_2023/RIXS/","Fe",[50:60]);