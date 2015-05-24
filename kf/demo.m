
clc
% 加载股票数据
% load('ch_stock.mat');
load('apple_stock.mat')
stockData = apple_stock;
% 绘制数据折线图
plot(stockData(:,1), stockData(:,2), '-O');
% 使用卡尔曼滤波预测股票价格
predictData = vdKFilter(stockData);
hold on
plot(predictData(:,1), predictData(:,2), 'r-O');
xlabel('时间')
ylabel('股价')
legend('实际值','预测值')

if size(predictData, 1) == size(stockData, 1)
    error = (stockData(2:end,2) - predictData(1:end-1,2));
else
    error = (stockData(2:end,2) - predictData(1:end,2));
end
% 计算与实际观测值的误差
errorMean = sqrt(mean(error.^2))
errorRateMean = sqrt(mean( (error./stockData(2:end,2)).^2) )
