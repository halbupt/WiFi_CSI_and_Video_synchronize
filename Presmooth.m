function [csi_ampsr,  csi_ampss]= Presmooth(csi_amps)
% remove the outlinears & smooth & wavelet decomposition 
[num, subcarrier, height,width] = size(csi_amps);
k = 10;
nsigma = 3;
n = 10; % smooth neighber
for ti = 1: height
    for ri = 1: width
        for nd= 1:subcarrier
            % hampel(x,k,nsigma) specifies a number of standard deviations, nsigma, by
            % which a sample of x must differ from the local median for it to be replaced
            % with the median. nsigma defaults to 3.
            csi_ampsr (:, nd, ti, ri)= hampel(squeeze(csi_amps(:, nd, ti, ri)), k, nsigma);
%             csi_phasr (:, nd, ti, ri)= hampel(squeeze(csi_phas(:, nd, ti, ri)), k, nsigma);
            
            % smooth data
            csi_ampss (:, nd, ti, ri)= smooth(squeeze(csi_ampsr(:, nd, ti, ri)), n);
%             csi_phass (:, nd, ti, ri)= smooth(squeeze(csi_phasr(:, nd, ti, ri)), n);
        end
    end
end