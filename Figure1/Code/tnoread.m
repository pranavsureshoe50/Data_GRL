function [num,var]=tnoread(file)

    fid = fopen(file,'r');
    data  = fscanf(fid, '%f',[2 inf]);
    
    var=data(1,:)'; num=data(2,:)';
    var(1)=[]; num(end)=[];
    
    aux = sortrows([num var],1);
    
    num = aux(:,1);
    var = aux(:,2);

end