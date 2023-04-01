from chefboost import Chefboost as chef
from multiprocessing import freeze_support
import pandas as pd
from numpy import random

# decision tree create

###############

class DecisionTrees:
    def create_model(self):
        model = chef.fit(pd.read_csv("data/db.txt"), {'algorithm': 'ID3'})
        return model

    def return_predict(self, mod):

        # read data
        #df = pd.read_csv("data/db.txt")

        # Header of df looks like:
        header = ['Size(bigger_more_difficult)', 'Year(older_more_difficult)', 'Protection_from_defuse',
                  'Meters_under_the_ground', 'Random_detonation_chance', 'Detonation_power_in_m',
                  'Decision']

        # print data
        # print(df.head())

        # ID3 config
        #config = {'algorithm': 'ID3'}
        # create decision tree

        # print predict
        # print(chef.predict(model, [1, 2022, 0, 0, 0, 10]))

        # random generate characteristics for mine
        size = random.randint(1, 10)
        year = random.randint(1941, 2022)
        protection = 0
        if year >= 2000:
            protection = random.choice([1, 0, 1])
        m_under_the_ground = random.randint(0, 10)
        detonation_chance = random.randint(0, 100)
        detonation_power_in_m = random.randint(0, 10)
        detonation_power_in_m = detonation_power_in_m - m_under_the_ground
        if detonation_power_in_m <= 0:
            detonation_power_in_m = 0

        mine_characteristics = [size, year, protection, m_under_the_ground, detonation_chance, detonation_power_in_m]

        # print data about mine
        print("Mine characteristics : ")
        cnt = 0
        for i in mine_characteristics:
            print(header[cnt], " = ", i)
            cnt += 1

        # return prediction
        return chef.predict(mod, mine_characteristics)
