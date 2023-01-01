function simple_gui

% Create UIFigure
f = figure('Position',[50 50 1024 768]);

% Construct the components.
bopen = uicontrol(f,'Style','pushbutton',...
    'String','Open','Position',[11 727 100 22],'Units','normalized',...
    'Callback',@bopen_Callback);

epath = uicontrol(f,'Style','edit',...
    'String','','HorizontalAlignment','left','Position',[121 727 890 22],'Units','normalized');

llist = uicontrol(f,'Style','listbox',...
    'Position',[11 50 170 670],'Units','normalized','max',10000);

aplot = axes(f,'Units','pixels','Position',[220 70 780 640],'Units','normalized');

bload = uicontrol(f,'Style','pushbutton',...
    'String','Load','Position',[11 17 100 22],'Units','normalized',...
    'Callback',@bload_Callback);

bxcorr = uicontrol(f,'Style','pushbutton',...
    'String','Xcorr','Position',[118 17 100 22],'Units','normalized',...
    'Callback',@bxcorr_Callback);

bsum = uicontrol(f,'Style','pushbutton',...
    'String','Sum','Position',[225 17 100 22],'Units','normalized',...
    'Callback',@bsum_Callback);

ezero = uicontrol(f,'Style','edit',...
    'String','0','HorizontalAlignment','right','Position',[330 17 178 22],'Units','normalized');

bzero = uicontrol(f,'Style','pushbutton',...
    'String','Shift','Position',[516 17 100 22],'Units','normalized',...
    'Callback',@bzero_Callback);

edisp = uicontrol(f,'Style','edit',...
    'String','1','HorizontalAlignment','right','Position',[620 17 178 22],'Units','normalized');

bdisp = uicontrol(f,'Style','pushbutton',...
    'String','Etrans','Position',[805 17 100 22],'Units','normalized',...
    'Callback',@bdisp_Callback);

bsave = uicontrol(f,'Style','pushbutton',...
    'String','Save','Position',[911 17 100 22],'Units','normalized',...
    'Callback',@bsave_Callback);

% Create the callbacks.
  function bopen_Callback(src,event)
    global dirname
    dirname = uigetdir();
    set(epath,'String',dirname);
    fileinfo = dir(dirname);
    set(llist,'String',{fileinfo.name});
  end

  function bload_Callback(src,event)
    global data
    global dirname
    namelist = get(llist,'String');
    numselect = get(llist,'Value');
    filelist = namelist(numselect);
    data = load_ccd(filelist,dirname);
    datanumber = size(data,1);
    cla;
    for i = 1:datanumber
      plot(data(i,:));
      hold on;
    end
    hold off;

  end

  function bxcorr_Callback(src,event)
    global data
    xlimit = get(aplot,'XLim');
    ylimit = get(aplot,'YLim');
    data = correlate_rixs(data,xlimit);
    datanumber = size(data,1);
    cla;
    for i = 1:datanumber
      plot(data(i,:));
      hold on;
    end
    set(aplot,'XLim',xlimit)
    set(aplot,'YLim',ylimit)
    hold off;

  end

  function bsum_Callback(src,event)
    global data
    global xdata
    global ydata
    datanumber = size(data,1);
    for i = 1:datanumber
      if i == 1
        ydata = data(i,:);
      else
        ydata = ydata+data(i,:);
      end
    end
    xdata = [1:length(ydata)];
    cla;
    plot(xdata,ydata);
  end

  function bzero_Callback(src,event)
    global xdata
    global ydata
    zero = str2num(get(ezero,'String'));
    xdata = xdata - zero;
    cla;
    plot(xdata,ydata);
  end

  function bdisp_Callback(src,event)
    global xdata
    global ydata
    dispersion = str2num(get(edisp,'String'));
    xdata = xdata .* dispersion;
    cla;
    plot(xdata,ydata);
  end

  function bsave_Callback(src,event)
    global xdata
    global ydata
    filename = uiputfile ({'*.txt', 'Text files'})
    dlmwrite(filename,[xdata;ydata].','delimiter','\t','-append');
  end


end



