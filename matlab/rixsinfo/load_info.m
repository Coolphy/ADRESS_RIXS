function info = load_info(filelist,dirname)
global info_dict;

info = {};
filenumber=length(filelist);

for i=1:filenumber
    filename = filelist{i};
    if ~isfield(info_dict,filename)
        try
            info_dict(1).(filename) = load_h5([dirname,'/',filename,'_d2.h5']);
        catch
            break
        end  
    end
    
    info{i,1}= info_dict(1).(filename).('ee');
    info{i,2}= info_dict(1).(filename).('pp');
    info{i,3}= info_dict(1).(filename).('tt');
    info{i,4}= info_dict(1).(filename).('xx');
    info{i,5}= info_dict(1).(filename).('yy');
    info{i,6}= info_dict(1).(filename).('zz');
    info{i,7}= info_dict(1).(filename).('thth');
    info{i,8}= info_dict(1).(filename).('phph');
    info{i,9}= info_dict(1).(filename).('tltl');
    info{i,10}= info_dict(1).(filename).('atat');
    info{i,11}= info_dict(1).(filename).('spsp');
    info{i,12}= info_dict(1).(filename).('slsl');
    info{i,13}= info_dict(1).(filename).('bcbc');
end
end
