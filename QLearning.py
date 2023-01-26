import csv


class QLearning:
    def UpdateQTable(self, reward: float, next_State: str, discount_Factor: float=1, learning_Rate: float=1):
        print()

    def GetQTable(self, file_Name: str):
        f = open(file_Name, "r")
        csv_r = csv.reader(f)
        q_table = []
        for line in csv_r:
            q_table.append(line)
        return q_table
