import BaskinRobbins31 as BR31
import QLearning as QL
import random


if __name__ == '__main__':
    br31 = BR31.BaskinRobbins31()
    #br31.StartLearning(100000, "BaskinRobbins31_Q.csv", 100)
    br31.StartGame("BaskinRobbins31_Q.csv", False)
