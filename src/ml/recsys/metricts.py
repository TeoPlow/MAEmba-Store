import pandas as pd
import numpy as np

def hit_rate_at_k(recommended_list:list, final_bought_list:list, k=5) -> int:
    """
    Вычисляет был ли куплен или было ли взаимодействие хоть с одним товаром из списка рекомендуемых.
    
    :param recommended_list: список рекомендаций 
    :param final_bought_list: список совершенных покупок 
    :param k: какое количество товаров учитываем
    :return: 0 если ничего из рекомендаций не было куплено, 1 иначе
    """
    final_bought_list = np.array(final_bought_list)
    recommended_list = np.array(recommended_list)
 
    flags = np.isin(recommended_list[:k], final_bought_list )
    hit_rate = int(flags.sum() > 0)
    return hit_rate

def precision_at_k(recommended_list:list, final_bought_list:list, k=5) -> float:
    """
    Вычисляет какой процент рекомендованных товаров юзер купил.

    :param recommended_list: список рекомендаций 
    :param final_bought_list: список совершенных покупок 
    :param k: какое количество товаров учитываем
    :return: процент рекомендованных товаров юзер купил
    """ 
    final_bought_list = np.array(final_bought_list)
    recommended_list = np.array(recommended_list)
 
    final_bought_list = final_bought_list 
    recommended_list = recommended_list[:k]
 
    flags = np.isin(recommended_list, final_bought_list)
    precision = flags.sum() / len(recommended_list)
    return precision
 
def money_precision_at_k(recommended_list:list, final_bought_list:list, prices_recommended:list, k=5) -> float:
    """
    Вычисляет какой процент доходов от рекомендованных товаров.

    :param recommended_list: список рекомендаций 
    :param final_bought_list: список совершенных покупок 
    :param prices_recommended: список цен
    :param k: какое количество товаров учитываем
    :return: процент рекомендованных товаров юзер купил
    """ 
    final_bought_list = np.array(final_bought_list)
    recommended_list = np.array(recommended_list)
    prices_recommended = np.array(prices_recommended)
 
    final_bought_list = final_bought_list  
    recommended_list = recommended_list[:k]
    prices_recommended = prices_recommended[:k]
 
    flags = np.isin(final_bought_list, recommended_list)
    precision = (flags * prices_recommended).sum() / prices_recommended.sum()
    return precision
