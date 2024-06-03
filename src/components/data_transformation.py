import sys
import numpy as np
import pandas as pd
import os

from mlxtend.preprocessing import TransactionEncoder
from sklearn.pipeline import Pipeline
from dataclasses import dataclass

from exception import CustomException
from logger import logging

@dataclass
class DataTransformationConfig:
    transformed_data_path = os.path.join('artifacts','data_transformed.csv')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def initiate_data_transformation(self,train_data):

        try:
            train_df = pd.read_csv(train_data)

            logging.info("Train data has been read")
            logging.info("Beginning trasformation process")
            train_df = train_df.drop(train_df[train_df['rating'].str.contains("\|")].index)
            train_df= train_df.dropna(subset='rating_count')

            text_attr = ['product_id','product_name','about_product']
            list_attr = ['category','user_id','user_name','review_id','review_title','review_content']
            float_attr = ['discounted_price','actual_price','discount_percentage','rating','rating_count']

            train_df[text_attr] = train_df[text_attr].astype('string')
            train_df[list_attr] = train_df[list_attr].apply(lambda x: x.str.split("[\|\,]"))
            for attr in float_attr:
                train_df[attr] = train_df[attr].apply(lambda x:x.replace("₹","").replace(",","").replace("%","")).astype('float')
            
            train_df['main_category'] = train_df['category'].str[0].astype("string")
            train_df['sub_category'] = train_df['category'].str[-1].astype("string")
            train_df['weighted_rating'] = train_df['rating']*train_df['rating_count']
            os.makedirs(os.path.dirname(self.data_transformation_config.transformed_data_path),exist_ok = True)
            train_df.to_csv(self.data_transformation_config.transformed_data_path,index = False, header = True)


            explode_df = train_df[['product_id','sub_category','user_id']].explode('user_id').drop_duplicates()
            asso_df = explode_df.groupby('user_id').agg({"product_id":list,"sub_category":list})
            asso_df['sub_category'] = asso_df['sub_category'].apply(lambda x:list(set(x)))
            asso_df = asso_df[asso_df['sub_category'].apply(len) > 1]

            a = TransactionEncoder()
            data_to_encode = list(asso_df['sub_category'])
            a_data = a.fit(data_to_encode).transform(data_to_encode)
            aprio_df = pd.DataFrame(a_data,columns = a.columns_)
            aprio_df = aprio_df.replace(False,0).replace(True,1)
            
            return aprio_df

        except Exception as e:
            raise CustomException(e,sys)


            
