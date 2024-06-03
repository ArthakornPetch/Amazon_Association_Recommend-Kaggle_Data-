import sys
import os
import pandas as pd
from src.exception import CustomException
from src.logger import logging

class PredictPipeline:
    def __init__(self):
        pass

    def create_recommend(self,sub_category):
        try:
            data_path = os.path.join("artifacts",'data_transformed.csv')
            rules_path = os.path.join("rules",'association_rules.csv')
            df = pd.read_csv(data_path)
            rules = pd.read_csv(rules_path)

            sorted_rules = rules.sort_values("lift", ascending=False)
            recommendation_list = []
            for i, product in sorted_rules["antecedents"].items():
                for j in list(product):
                    if j == sub_category:
                        recommendation_list.append(list(sorted_rules.iloc[i]["consequents"])[0])
            if len(recommendation_list) > 1:
                recommended_items = df[df['sub_category'].isin(recommendation_list)].sort_values(by='weighted_rating',ascending = False)[['product_id','product_name','about_product','actual_price','discounted_price','rating','img_link','product_link']]
            else: recommended_items = df[df['sub_category'] == sub_category].sort_values(by='weighted_rating',ascending = False)[['product_id','product_name','about_product','actual_price','discounted_price','rating','img_link','product_link']]
            return recommended_items.iloc[0:5,:]
        except Exception as e:
            raise CustomException(e,sys)