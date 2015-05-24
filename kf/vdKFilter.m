function N_predict = vdKFilter(N)
% 以实际股票观测序列为输入，通过对其进行分形建模得到X_observed，
% 再利用卡尔曼滤波遍历X_observed中每个时刻的值，并预测下一时刻
% 的值，最后将预测值输出。

m = size(N,1);
% 参数初始化
Phi = [1 log(1/4);0 1];
Gamma = [log(1/2) 1]';
Q = 1e-4;
R = 1.0;
% 最优预测值
x_perfect = log(N(1,2)/N(2,2))*[1 1/log(2)]';
x_predict = 0; % 预测值
P_perfect = 1e-4*eye(2);
P_predict = 0;
X_predict = zeros(m,1); % 预测值序列
% 分形观测序列
X_observed = log(N(1:end-1,2)./N(2:end,2)); 
C = [1, 0];
epsilon = 0;

for k = 1:m
    x_predict = Phi * x_perfect;
    X_predict(k) = x_predict(1,1);
    if k == m
        break;
    end
    epsilon = X_observed(k) - C*x_predict;
    P_predict = Phi*P_perfect*Phi' + Gamma*Q*Gamma';
    K = P_predict * C' * 1/(C*P_predict*C' +R);
    P_perfect = (1 - K*C) * P_predict;
    x_perfect = x_predict + K*epsilon;
    
    Phi = [1 log( ((k+1)^2-1)/(k+1)^2 ); 0 1];
    Gamma = [log(k/(k+1)) 1];
end

N_predict = zeros(m, size(N,2));
N_predict(:,1) = 1 + N(:,1);
N_predict(:,2) = N(:,2)./exp(X_predict);

end
