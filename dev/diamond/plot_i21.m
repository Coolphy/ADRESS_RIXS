
clear all;
fitpara = [];

%%
%     filepath = 'D:\Reaserch\Data\RIXS\DIAMOND\CuSb2O6\qmap_lv\';
%     prefix = 'qmap_lv-';
%     subfix = '.dat';
%     for i = 0:28
%         filename = make_name(prefix,i,subfix);
%         [X,Y]=load_data(filepath,filename);
%         plot(X( X > -0.1 & X < 0.2),Y( X > -0.1 & X < 0.2)+i*0.5);
%         hold on;
%     end
%     xlabel('[H, H, 0] ( r.l.u. )') 
%     ylabel('Intensity ( arb. u. )') 
%     legend({'Q-scan LV [110]'})   

%%
% filepath = 'D:\Reaserch\Data\RIXS\DIAMOND\CuSb2O6\qmap_lv\';
% prefix = 'qmap_lv-';
% subfix = '.dat';
% 
% 
% for i = 0:1:28
%     filename = make_name(prefix,i,subfix);
%     [X,Y]=load_data(filepath,filename);
%         plot(X( X > -0.2 & X < 0.2)+(i-1)*0.03*sqrt(2)-0.42*sqrt(2),Y( X > -0.2 & X < 0.2));
%     fitpara(i+1,:) = fit_elastic(X,Y);
%     fitresult = fit_elastic(X,Y);
% %     plot(X - fitresult(2),Y - fitresult(1) * exp(-log(2) * (X-fitresult(2)).^2 / fitresult(3).^2));
% %     plot(X - fitresult(2),Y)
%     hold on;
% end
% xlabel('Energy Loss ( eV )') 
% ylabel('Intensity ( arb. u. )') 
% legend({'Q-scan LV [110]'})

%%
% filepath = 'D:\Reaserch\Data\RIXS\DIAMOND\CuSb2O6\Emap\';
% prefix = 'Emap-';
% subfix = '.dat';
% for i = 0:1:10
%     filename = make_name(prefix,i,subfix);
%     [X,Y]=load_data(filepath,filename);
%     fitresult = fit_elastic(X( X > -0.2 & X < 0.2),Y( X > -0.2 & X < 0.2));
% %         scatter(X( X > -0.2 & X < 0.2) - fitresult(2),Y( X > -0.2 & X < 0.2),1);
%     plot(X - fitresult(2),Y - fitresult(1) * exp(-log(2) * (X-fitresult(2)).^2 / fitresult(3).^2) +i*0.2)
%     hold on;
% end
% hold off;
% legend({'927.1 eV','927.3 eV','927.5 eV','927.7 eV','927.9 eV','928.1 eV','928.3 eV','928.5 eV','928.7 eV','928.9 eV','929.1 eV'})
% xlabel('Energy Loss ( eV )') 
% ylabel('Intensity ( arb. u. )') 

%%
% filepath = 'D:\Reaserch\Data\RIXS\DIAMOND\CuSb2O6\th2th_lh\';
% prefix = 'Untitled-';
% subfix = '.dat';
% for i = 0:1:8
%     filename = make_name(prefix,i,subfix);
%     [X,Y]=load_data(filepath,filename);
%     [X,Y] = find_elastic(X,Y);
%     plot(X,Y);
%     hold on;
% %     fitresult = fit_elastic(X( X > -0.2 & X < 0.2),Y( X > -0.2 & X < 0.2));
% %     fitpara(i+1,:) = fit_elastic(X,Y);
% %     plot(X - fitresult(2),Y - fitresult(1) * exp(-log(2) * (X-fitresult(2)).^2 / fitresult(3).^2))
%     hold on;
% end
% hold off;
% legend({'0.15','0.20','0.225','0.25','0.275','0.30','0.35','0.40','0.47'})
% xlabel('Energy Loss ( eV )') 
% ylabel('Intensity ( arb. u. )') 

%%
% filepath = 'D:\Reaserch\Data\RIXS\DIAMOND\CuSb2O6\qmap_pi0_lh\';
% prefix = 'Untitled-';
% subfix = '.dat';
% 
% for i = 0:1:28
%     filename = make_name(prefix,i,subfix);
%     [X,Y]=load_data(filepath,filename);
%     I0 = trapz(X( X > 0.1 & X < 0.8),Y( X > 0.1 & X < 0.8));
%         plot(X( X > -0.2 & X < 0.2)+(i-1)*0.03*sqrt(2)-0.42*sqrt(2),Y( X > -0.2 & X < 0.2)/-I0);
%     fitpara(i+1,:) = fit_elastic(X,Y);
%     fitresult = fit_elastic(X,Y);
% %     plot(X - fitresult(2),Y - fitresult(1) * exp(-log(2) * (X-fitresult(2)).^2 / fitresult(3).^2)+i*0.3);
% %     plot(X - fitresult(2),Y/-I0)
%     hold on;
% end
% xlabel('Energy Loss ( eV )') 
% ylabel('Intensity ( arb. u. )') 
% legend({'Q-scan LH [100]'})

%%
% filepath = 'D:\Reaserch\Data\RIXS\DIAMOND\CuSb2O6\qmap_pimpi_lh\';
% prefix = 'qmap_pimpi_lh-';
% subfix = '.dat';
% 
% for i = 0:1:28
%     filename = make_name(prefix,i,subfix);
%     [X,Y]=load_data(filepath,filename);
% %     plot(X( X > 0.8 & X < 1.8)+(i)*0.03-0.42,Y( X > 0.8 & X < 1.8));
%     fitpara(i+1,:) = fit_elastic(X,Y);
%     fitresult = fit_elastic(X,Y);
% %     plot(X - fitresult(2),Y - fitresult(1) * exp(-log(2) * (X-fitresult(2)).^2 / fitresult(3).^2)+i*0.3);
%     I0 = trapz(X( X > 0.1 & X < 0.8),Y( X > 0.1 & X < 0.8));
%     plot(X +(i-1)*0.03-0.42 - fitresult(2),Y/-I0)
%     hold on;
% end
% xlabel('Energy Loss ( eV )') 
% ylabel('Intensity ( arb. u. )') 
% legend({'Q-scan LH [1 -1 0]'})

%%

% filepath = 'D:\Reaserch\Data\RIXS\DIAMOND\CuSb2O6\qmap_pipi2_lh\';
% prefix = 'qmap_pipi2_lh-';
% subfix = '.dat';
% 
% for i = 0:1:28
%     filename = make_name(prefix,i,subfix);
%     [X,Y]=load_data(filepath,filename);
%         plot(X( X > -0.2 & X < 0.2)+(i-1)*0.03-0.42,Y( X > -0.2 & X < 0.2));
%     fitpara(i+1,:) = fit_elastic(X,Y);
%     fitresult = fit_elastic(X,Y);
% %     plot(X - fitresult(2),Y - fitresult(1) * exp(-log(2) * (X-fitresult(2)).^2 / fitresult(3).^2)+i*0.3);
% %     plot(X - fitresult(2),Y)
%     hold on;
% end
% xlabel('Energy Loss ( eV )') 
% ylabel('Intensity ( arb. u. )') 
% legend({'Q-scan LH phi = 22.5'})

%%
% filepath = 'D:\Reaserch\Data\RIXS\DIAMOND\CuSb2O6\qmap_pipi4_lh\';
% prefix = 'qmap_pipi4_lh-';
% subfix = '.dat';
% 
% for i = 0:1:28
%     filename = make_name(prefix,i,subfix);
%     [X,Y]=load_data(filepath,filename);
%         plot(X( X > -0.2 & X < 0.2)+(i-1)*0.03-0.42,Y( X > -0.2 & X < 0.2));
%     fitpara(i+1,:) = fit_elastic(X,Y);
%     fitresult = fit_elastic(X,Y);
% %     plot(X - fitresult(2),Y - fitresult(1) * exp(-log(2) * (X-fitresult(2)).^2 / fitresult(3).^2)+i*0.3);
% %     plot(X - fitresult(2),Y)
%     hold on;
% end
% xlabel('Energy Loss ( eV )') 
% ylabel('Intensity ( arb. u. )') 
% legend({'Q-scan LH phi = 22.5'})

%%
filepath = 'D:\Reaserch\Data\RIXS\DIAMOND\CuSb2O6\HT_pipi_lh\';
prefix = 'Untitled-';
subfix = '.dat';

for i = 0:1:28
    filename = make_name(prefix,i,subfix);
    [X,Y]=load_data(filepath,filename);
    I0 = trapz(X( X > 0.1 & X < 0.8),Y( X > 0.1 & X < 0.8));
    plot(X( X > -0.2 & X < 0.2)+(i-1)*0.03-0.42,Y( X > -0.2 & X < 0.2));
    fitpara(i+1,:) = fit_elastic(X,Y);
    fitresult = fit_elastic(X,Y);
%     plot(X - fitresult(2),Y - fitresult(1) * exp(-log(2) * (X-fitresult(2)).^2 / fitresult(3).^2)+i*0.3);
%     plot(X - fitresult(2),Y/-I0)
    hold on;
end
xlabel('Energy Loss ( eV )') 
ylabel('Intensity ( arb. u. )') 
legend({'Q-scan LH [100]'})

















%%
function filename = make_name(prefix,runnumber,subfix)
    filename = [prefix,sprintf('%02d',runnumber),subfix];
end

function [X,Y]=load_data(filepath,filename)
    name = [filepath,filename];
    data = importdata([filepath,filename],'\t',2);
    X = data.data(:,1);
    Y = data.data(:,2);
end

function fpara = fit_elastic(X,Y)
    fitfunction = 'a1 * exp(-log(2) * (x-xc1)^2 / dx1^2) + a2 * exp(-log(2) * (x-xc2)^2 / dx2^2)';
    ft = fittype(fitfunction, 'independent','x','coefficients', {'a1', 'xc1', 'dx1','a2','xc2','dx2'});
    fo = fitoptions('Method','NonlinearLeastSquares',...
               'Lower',[0, -0.05, 0.018, 0, -0.02, 0.018],...
               'Upper',[Inf, 0.1, 0.019, Inf, 0.1 0.1],...
               'StartPoint',[15, 0, 0.19, 3, 0.04, 0.45]);
    [curve,gof] = fit(X,Y,ft,fo);
    fpara=coeffvalues(curve);
end

function [xdata,ydata]=find_elastic(xdata,ydata)
    [pks,locs,w,p] = findpeaks(ydata,'MinPeakHeight',5,'MinPeakProminence',5,'MinPeakWidth',0.005);
    zeropixel = xdata(locs(size(locs,1)));
%     zeropixel = xdata(locs(1));
    xdata = xdata - zeropixel;
end