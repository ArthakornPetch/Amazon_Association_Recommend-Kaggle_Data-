import os
import sys
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
from mlxtend.frequent_patterns import apriori, association_rules

@dataclass
class ModelTrainerConfig:
    trained_file_path=os.path.join("rules","association_rules.csv")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()
    
    def initiate_model_create(self,aprio_df):

        try:
            logging.info("Start creating association rules")
            aprio_rules = apriori(aprio_df, min_support = 0.005,use_colnames = True, verbose = 1)
            asso_rules = association_rules(aprio_rules,metric = 'confidence',min_threshold = 0.3)
            logging.info("Saving association rules....")
            os.makedirs(os.path.dirname(self.model_trainer_config.trained_file_path),exist_ok = True)
            asso_rules.to_csv(self.model_trainer_config.trained_file_path,index = False, header = True)
            return asso_rules
        except Exception as e:
            raise CustomException(e,sys)
