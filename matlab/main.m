%%
addpath("/sls/X03MA/Data1/x03maop/RIXS/Wei_e20799/FePS3_Feb_2023/");
global rixs_struct
rixs_struct = struct([]);

%%
[en, tey, tfy] = plot_xas("/sls/X03MA/Data1/x03maop/RIXS/Wei_e20799/FePS3_Feb_2023/XAS/", "Fe", 18);

%%
[x, y] = plot_rixs("/sls/X03MA/Data1/x03maop/RIXS/Wei_e20799/FePS3_Feb_2023/RIXS/", "Fe", [50:60]);
