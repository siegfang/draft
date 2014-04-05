import random
import math
import collections
import datetime
import math

def get_user_brands(reco_file_path, end_date):
    '''用户商品倒插表'''
    beta = 0.5
    reco_file=open(reco_file_path,"r")
    reco_file.readline()
    brand_pref = collections.defaultdict(lambda :0)
    for line in reco_file:
        line = line.strip()
        user_name, brand_id, behavior_id, date_str = tuple(line.split(","))

        cur_date = datetime.date(2013,
            int(date_str[0:date_str.find('月')]),
            int(date_str[date_str.find('月')+1:-1]))
        # 流行度
        popularity = 1 / (1 + beta * (end_date - cur_date).days)
        brand_pref[brand_id] += popularity
        # print(brand_pref)

    pref_thres = 1.5
    # print(brand_pref)
    # brand_pref = {brand_id:pref for brand_id, pref in brand_pref.items() if pref > pref_thres }
    item_pool = [brand_id for brand_id, pref in brand_pref.items() if pref > pref_thres]

    reco_file=open(reco_file_path,"r")
    reco_file.readline()

    user_brands = collections.defaultdict(lambda :
        collections.defaultdict(lambda :0))
    # brand_users = collections.defaultdict(lambda :
    #     collections.defaultdict(lambda :0))

    mu, record_time = 0, 0

    for line in reco_file:
        line = line.strip()
        user_name, brand_id, behavior_id, date_str = tuple(line.split(","))

        # if behavior_id == '1' or behavior_id == '0':
        if behavior_id == '1':
            user_brands[user_name][brand_id] += 1
            mu += 1
        else:
            user_brands[user_name][brand_id] += 0
            mu += 0
        # brand_users[brand_id][user_name] += 1
        record_time += 1

    mu /= record_time

    # for user_name, brand_ids in user_brands.items():
    #     print(user_name, brand_ids)

    return (user_brands, item_pool, mu)


def init_model(user_brands, K):
    '''初始化偏置LFM'''

    P = {key:[random.random()/math.sqrt(K) for x in range(K)]
        for key in user_brands.keys()}
    bu = {key:0 for key in user_brands.keys()}

    brand_keys = set()
    for user_name, brand_id_dict in user_brands.items():
        for brand_id in brand_id_dict:
            brand_keys.add(brand_id)

    Q = {key:[random.random()/math.sqrt(K) for x in range(K)]
        for key in brand_keys}
    bi = {key:0 for key in brand_keys}
    y = {key:[random.random()/math.sqrt(K) for x in range(K)]
        for key in brand_keys}

    return (P, Q, bu, bi, y)

def preference(user, brand, history_brand, y, p, q, bu, bi, mu):
    '''用户对品牌的兴趣'''
    pref = mu + bu[user] + bi[brand]
    
    nei_sum = p[user]
    for brand in history_brand:
        nei_sum = [nei_sum[idx] + y[brand][idx] for idx in range(0, len(p[user]))]
    pref += sum(q[brand][f]*nei_sum[f] for f in range(0, len(q[brand])))
    return pref    

def select_samples(items, item_pool, ratio):
    '''随机选择负样本'''

    ret = {key:1 for key, buy_time in items.items() if buy_time >= 1}

    samples_size = ratio * len(ret)
    for i in range(0, int(len(ret) * ratio/2)):
        item = item_pool[random.randint(0,len(item_pool)-1)]
        if item in ret:
            continue
        ret[item] = 0
        if len(ret) > samples_size:
            break
    return ret

def svd_plus(user_brands, item_pool, ratio, K, mu, step_time, alpha, lamb):
    '''隐语义模型'''
    P, Q, bu, bi, y = init_model(user_brands, K)
    z = {}
    for step in range(0, step_time):
        print('training......', step)
        for user, brands in user_brands.items():
            z[user] = P[user]
            ru = 1 / math.sqrt(1.0 * len(brands))
            samples = select_samples(brands, item_pool, ratio)
            for item, rui in samples.items():
                z[user] = [z[user][idx] + y[item][idx]*rui for idx in range(0, K)]
            
            temp_sum = [0 for idx in range(0, K)]
            for item, rui in samples.items():
                eui = rui - preference(user, item, brands, y, P, Q, bu, bi, mu) 
                bu[user] += alpha * (eui - lamb * bu[user])
                bi[item] += alpha * (eui - lamb * bi[item])
                for f in range(0, K):
                    temp_sum[f] += Q[item][f] * eui * rui
                    P[user][f] += alpha * (eui * Q[item][f] - lamb * P[user][f])
                    Q[item][f] += alpha * (z[user][f] +\
                        eui * P[user][f] - lamb * Q[item][f])
            for item, rui in samples.items():
                y[item] += [alpha*(temp_sum[idx] - lamb * y[item][idx]) for idx in range(0, K)]

        alpha *= 0.9
        # print(Q['7868'])
    # 归一化
    # for key, values in P.items():
    #     m = math.sqrt(sum(value*value for value in values))
    #     P[key] = [value/m for value in values]

    # for key, values in Q.items():
    #     m = math.sqrt(sum(value*value for value in values))
    #     Q[key] = [value/m for value in values]

    # print(Q['7868'])

    return (P, Q, bu, bi, y)

def recommend(user, history_brand, y, P, Q, bu, bi, mu):
    '''推荐'''

    rank = {brand:preference(user, brand, history_brand, y, P, Q, bu, bi, mu)
        for brand, q in Q.items()}

    return rank

    
if __name__ == '__main__':

    ali_file_path = "E:\作业汇总\学术会议及讲座\天池\data\\t_alibaba_data.csv"
    data_file_path = "E:\作业汇总\学术会议及讲座\天池\data\data_4_7_15.txt"
    result_file_path = "E:\作业汇总\学术会议及讲座\天池\\result\lfm_7_15.txt"
    result_file = open(result_file_path, 'w')

    # data_file_path = "Z:\CodeSpace\Python\天池\data\\test.txt"

    ratio, K, step_time, alpha, lamb = 3, 10, 200, 0.02, 0.02

    user_brands, item_pool, mu\
        = get_user_brands(data_file_path, datetime.date(2013, 7, 15))

    P, Q, bu, bi, y = svd_plus(user_brands, item_pool, ratio, K, mu, step_time, alpha, lamb)

    rank_thres = 0.7

    print("recommending...")

    for user_name, brands in user_brands.items():
        rank = recommend(user_name, brands, y, P, Q, bu, bi, mu)
        
        rank = {brand:pref for brand, pref in rank.items() if pref > rank_thres}
        # print(rank)

        commit_brand = sorted(rank.items(), key=lambda d:d[1], reverse = True)[:10]
        # if len(commit_brand) > 1 and commit_brand[0][0] == '27791' and commit_brand[0][1] < 0.7:
        #     commit_brand = commit_brand[1:11]
        # else:
        #     commit_brand = commit_brand[:10]
        commit_brand = [brand for brand, pref in commit_brand]
        

        if len(commit_brand) < 1:
            continue

        result_file.write(user_name + '\t' + ','.join(commit_brand) + '\n')
        # print(sorted_rank[:10])
