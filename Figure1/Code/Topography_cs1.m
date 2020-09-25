clear; format long; clc; close all;


%% Parameters of stl
filename = './Current_pp.stl' ;
[p,t,tnorm] = stlread(filename,1); % (vertices of each point) , (point num for each point), ...
                                      %normal vector
                                   
trin=length(tnorm); 
normx=tnorm(:,1);normy=tnorm(:,2);normz=tnorm(:,3);

% x is vertical, y is streamwise , z spanwise
vertexx = p(:,1);
vertexy = p(:,2);
vertexz = p(:,3);

% centre of triangles
vertexc = zeros(trin,3); tri_area= zeros(trin,1); 

for i = 1:trin
    
        vertexc(i,:) = 1/3*(p(t(i,1),:)+p(t(i,2),:)+p(t(i,3),:));
        tri_area(i,1) = area3D([p(t(i,1),1) p(t(i,2),1) p(t(i,3),1)], ...
            [p(t(i,1),2) p(t(i,2),2) p(t(i,3),2)], ...
            [p(t(i,1),3) p(t(i,2),3) p(t(i,3),3)] ) ;
    
end

% All parameters of the stl file computed
%% Domain
% Conventions of the paper

Lx_start = -1000 ;
Lx_end   =  2000 ; Lx = Lx_end - Lx_start ;

Ly_start =  -1000 ;
Ly_end   =  1000  ; Ly = Ly_end - Ly_start ;

Lz_start =  -0.0 ;
Lz_end   =  150 ; Lz = Lz_end - Lz_start ;

% new points
  points =  p  ;
  points(:,1) = p(:,3);
  points(:,2) = -p(:,2);
  points(:,3) = p(:,1);
  
  faces = t  ;
  faces(:,1) = t(:,3);
  faces(:,3) = t(:,1);

%% Visuallisation
%figure('rend','painters','pos',[10 10 900 600])
f1 = figure ;
set(gcf, 'Position',  [100, 100, 1000, 400])
cmap = copper(256); %get current colormap
cmap=cmap([40:192],:); % set your range here
rectangle('Position',[Lx_start Ly_start Lx_end-Lx_start Ly_end-Ly_start], ...
    'FaceColor',cmap(1,:),'EdgeColor','none',...
    'LineWidth',3)


axis([0 10 0 10])
h = patch('Faces',faces,'Vertices',points,'FaceVertexCData',points(:,3),'FaceColor','flat');
set(h,'edgecolor','none')%,'facecolor',[.19 .09 .0])

colormap(cmap); % apply new colormap
c=colorbar('Ticks',[0,75,150],...
         'TickLabels',{'0','0.5','1'},'location','southoutside');
caxis([0 150])     

x1=get(gca,'position');
x=get(c,'Position');
x(3)=0.5; x(4) = 0.08;

set(c,'Position',x)
set(gca,'position',x1)

view([0.1 0.5 1])    % change the orientation
set(gca,'BoxStyle','full','Box','off')

xlim([Lx_start Lx_end])
ylim([Ly_start Ly_end])
zlim([Lz_start Lz_end])
grid off

daspect([.5 1 1])
axis normal
pbaspect([Lx/Lz Ly/Lz 1 ])
view(17, 14);
set(gca,'fontsize',20)
ax = gca ;
ax.LineWidth = 1 ;
ax.GridLineStyle = '--' ;
ax.GridColor = [.5 .5 .5] ;
ax.GridAlpha = 1 ;
axis off

% Create textbox
annotation(f1,'textbox',...
    [0.232 0.262 0.371 0.062],...
    'Interpreter','Latex','String',{'Bathymetric elevation $(z/h)$'},...
    'LineStyle','none','Fontsize',22,'FitBoxToText','off');


% Create textarrow
annotation(f1,'textarrow',[0.107 0.205],[0.4825 0.4625],...
    'Color',[0.35 0.35 0.35],...
    'LineWidth',2,...
    'FontSize',16);

% Create textarrow
annotation(f1,'textarrow',[0.106 0.191],[0.4825 0.655],...
    'Color',[0.35 0.35 0.35],...
    'LineWidth',2,...
    'FontSize',16);

% Create textarrow
annotation(f1,'textarrow',[0.106 0.106],[0.48103488372093 0.68],...
    'Color',[0.35 0.35 0.35],...
    'LineWidth',2,...
    'FontSize',16);

% Create textbox
annotation(f1,'textbox',[0.142 0.4715 0.001 0.00099999999999989],...
    'String','x','Fontsize',20,'Interpreter','Latex',...
    'FitBoxToText','off');

% Create textbox
annotation(f1,'textbox',[0.148 0.6815 0.001 0.00099999999999989],...
    'String','y','Fontsize',20,'Interpreter','Latex',...
    'FitBoxToText','off');

% Create textbox
annotation(f1,'textbox',...
    [0.0860000000000001 0.634 0.001 0.00099999999999989],'String','z',...
    'Fontsize',20,'Interpreter','Latex','FitBoxToText','off');
% Create doublearrow
annotation(f1,'doublearrow',[0.467 0.584],[0.8015 0.78],'LineWidth',4);


% Create arrow
annotation(f1,'arrow',[0.277 0.361],[0.824 0.8075],'LineWidth',3);

% Create textbox
annotation(f1,'textbox',...
    [0.502923192319232 0.820296355672261 0.0550768076807678 0.0627906964961876],...
    'String','$U_t=0.1$m/s',...
    'LineStyle','none',...
    'Interpreter','latex',...
    'FontSize',24,...
    'FitBoxToText','off');

% Create textbox
annotation(f1,'textbox',...
    [0.289923192319233 0.837796355672261 0.0550768076807678 0.0627906964961876],...
    'String','$U_c=0.1$m/s','LineStyle','none',...
    'Interpreter','latex',...
    'FontSize',24,...
    'FitBoxToText','off');




% Print if needed
 print('hill_tac', '-depsc2',  '-loose')
print('/home/pranav/Dropbox/Pranav_Masoud_Sutanu/my_journal_papers/Pranav_Sutanu_Geno_GRL2020/Pranav_v1/domain/h2','-depsc2',  '-loose')



