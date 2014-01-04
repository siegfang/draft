load fisheriris                     
data = [meas(:,1), meas(:,2)];            % Load Data
groups = ismember(species,'setosa');      % the labels of data
% partition the data for training and testing
[train, test] = crossvalind('holdOut',groups);
trainData = data(train,:);
testData = data(test,:);
trainGroups = groups(train);
cp = classperf(groups);
%============================== SVM method ================================
svmStruct = svmtrain(data(train,:),groups(train),...
                     'showplot',true, 'boxconstraint', 1e6);
classes = svmclassify(svmStruct,data(test,:),'showplot',true);
% svmclasses = logical(svmclasses);
% plot real classes
hold on
plot(data(groups,1), data(groups,2), 'gO', 'markersize',10);
hold on
plot(data(~groups,1), data(~groups,2), 'rs', 'markersize',10);
title('SVM - Binary Classification')
% evaluate the performance of the classifier
classperf(cp,classes,test);
cp.CorrectRate

%=============================== KNN method ===============================
ned = knnsearch(data(train,:), data(test,:), 'k', 5);
candidates = double(trainGroups(ned));   % get classes of the neighbours
% choose the class which appear more
knnClasses = logical(mode(candidates, 2));
% plot the data of training and test
figure
plot(trainData(trainGroups,1), trainData(trainGroups,2), 'g*');
hold on
plot(trainData(~trainGroups,1), trainData(~trainGroups,2), 'r+');
hold on
plot(testData(knnClasses,1), testData(knnClasses,2), 'm*');
hold on
plot(testData(~knnClasses,1), testData(~knnClasses,2), 'b+');
legend('1(training)', '0(training)', '1(classified)', '0(classified)')
% plot real classes
hold on
plot(data(groups,1), data(groups,2), 'gO', 'markersize',10);
hold on
plot(data(~groups,1), data(~groups,2), 'rd', 'markersize',10);
title('KNN(5) - Binary Classification')
% evaluate the performance of the classifier
classperf(cp,double(knnClasses),test);
cp.CorrectRate

% please be unannoted when you find code above output wrong result
% 逐步测试程序
% for i = 1:size(testData, 1)
%     hold on
%     plot(testData(i,1), testData(i,2), 'b*')
%     line(trainData(ned(i,:),1),trainData(ned(i,:),2),'color',[.5 .5 .5],'marker','o',...
%          'linestyle','none','markersize',10);
%     if knnClasses(i) == 1
%         plot(testData(i,1), testData(i,2), 'mO');
%     else
%         plot(testData(i,1), testData(i,2), 'c+');
%     end
% end


%========== Less Training instance and More Test instance =================
% repartition the data for transductive method
train = (data(:,1)>=4.5 & data(:,1)<=5 & groups(:)==1) ...
        | (data(:,1)>=6.75 & data(:,1)<=7.25 & groups(:)==0);
test = ~train;
trainData = data(train,:);
testData = data(test,:);
trainGroups = groups(train);
cp = classperf(groups);

%============================== SVM method ================================
svmStruct = svmtrain(data(train,:),groups(train),...
                     'showplot',true, 'boxconstraint', 1e6);
classes = svmclassify(svmStruct,data(test,:),'showplot',true);
% plot real classes
hold on
plot(data(groups,1), data(groups,2), 'gO', 'markersize',10);
hold on
plot(data(~groups,1), data(~groups,2), 'rs', 'markersize',10);
title('SVM - Binary Classification')
% evaluate the performance of the classifier
classperf(cp,classes,test);
cp.CorrectRate

%=============================== KNN method ===============================
ned = knnsearch(data(train,:), data(test,:), 'k', 5);
candidates = double(trainGroups(ned));   % get classes of the neighbours
% choose the class which appear more
knnClasses = logical(mode(candidates, 2));
% plot the data of training and test
figure
plot(trainData(trainGroups,1), trainData(trainGroups,2), 'g*');
hold on
plot(trainData(~trainGroups,1), trainData(~trainGroups,2), 'r+');
hold on
plot(testData(knnClasses,1), testData(knnClasses,2), 'c*');
hold on
plot(testData(~knnClasses,1), testData(~knnClasses,2), 'm+');
legend('1(training)', '0(training)', '1(classified)', '0(classified)')
hold on
% plot real classes
plot(data(groups,1), data(groups,2), 'gO', 'markersize',10);
hold on
plot(data(~groups,1), data(~groups,2), 'rs', 'markersize',10);
title('KNN(5) - Binary Classification')
% evaluate the performance of the classifier
classperf(cp,double(knnClasses),test);
cp.CorrectRate

%========================= Transductive SVM ===============================
tsvmGroups = double(groups);
tsvmGroups(tsvmGroups==0) = -1;   % set label for {1, -1}
tsvmGroups(test,:) = 0;
% pick the No.16 and No.84 data for initial cluster point
startdata = data([16, 84],:);    % 选取第16、第84个观测为初始凝聚点
% use Euclidean for k-means clustering
kmeansGroupsIdx = kmeans(data,2, 'Distance','sqEuclidean',...
                'Start',startdata);
% set cluster labels with the label which is more in one cluster
clusterLabels = [sum(tsvmGroups(kmeansGroupsIdx==1));...
                    sum(tsvmGroups(kmeansGroupsIdx==2))];
clusterLabels = sign(clusterLabels);
tsvmGroups(kmeansGroupsIdx==1) = clusterLabels(1);
tsvmGroups(kmeansGroupsIdx==2) = clusterLabels(2);
tsvmGroups(tsvmGroups==-1) = 0;
% select data with probability in 0.1
tsvmTrainIdx = rand(size(data,1),1)>0.9;
% tsvmTrainData = data(tsvmTrainIdx);

svmStruct = svmtrain(data(tsvmTrainIdx,:),tsvmGroups(tsvmTrainIdx),...
                     'showplot',true, 'boxconstraint', 1e6);
classes = svmclassify(svmStruct,data(test,:),'showplot',true);
hold on
plot(data(tsvmTrainIdx & tsvmGroups,1),...
     data(tsvmTrainIdx & tsvmGroups,2), 'g*');
hold on
plot(data(tsvmTrainIdx & ~tsvmGroups,1),...
     data(tsvmTrainIdx & ~tsvmGroups,2), 'r+');
hold on
% plot real classes
plot(data(groups,1), data(groups,2), 'gO', 'markersize',10);
hold on
plot(data(~groups,1), data(~groups,2), 'rs', 'markersize',10);
title('K-means(sqEuclidean) & TSVM - Binary Classification')
% evaluate the performance of the classifier
classperf(cp,classes,test);
cp.CorrectRate
