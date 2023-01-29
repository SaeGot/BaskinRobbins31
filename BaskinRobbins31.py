import random
import QLearning as QL

class BaskinRobbins31:
    def __init__(self):
        self.qLearning = QL.QLearning()

    def StartGame(self, q_TableFileName: str, player_First: bool=True, adjustAI: bool=True):
        self.qLearning.Initialize(q_TableFileName)
        print("게임 시작합니다.")
        current_number = 0
        player_turn = player_First

        if player_First == False:
            # 상대 턴
            player_turn = False
            current_number = self.__GetAINumber(current_number, adjustAI)
            print(current_number)
            player_turn = not player_turn

        while True:
            # 플레이어 턴
            if player_turn:
                current_number = self.__InputNumber(current_number)
            # 상대 턴
            else:
                current_number = self.__GetAINumber(current_number, adjustAI)
                print(current_number)
            if self.__CheckGameOver(current_number) == True:
                break
            else:
                player_turn = not player_turn

        if player_turn == False:
            print("승리")
        else:
            print("패배")

    def StartLearning(self, epoch: int, q_TableFileName: str, reward: float, learning_Rate: float = 0.01, discount_Factor: float = 1,
                      epsilon_GreedyDecayRate: float = 0.99999):
        self.qLearning.Initialize(q_TableFileName, True)
        n = 0
        epsilon_greedy = 1.0
        is_FirstPlayer = True
        while n < epoch:
            self.qLearning.Learn("0", "31", is_FirstPlayer, reward, learning_Rate, discount_Factor, epsilon_greedy)
            is_FirstPlayer = not is_FirstPlayer
            epsilon_greedy *= epsilon_GreedyDecayRate
            n += 1
            if n % 10000 == 0:
                print(n, "번째 학습중")
        self.qLearning.WriteQTable(q_TableFileName)

    def __GetAINumber(self, current_Number: int, adjustAI: bool) -> int:
        number = 0
        if adjustAI:
            number = self.__GetBestNumber(current_Number)
        else:
            number = self.__GetRandomNumber(current_Number)

        if number > 31:
            number = 31

        return number

    def __GetBestNumber(self, current_Number: int) -> int:
        return current_Number + int(self.qLearning.GetBestAction(str(current_Number)))

    def __GetRandomNumber(self, current_Number: int) -> int:
        return current_Number + random.randint(1, 3)

    def __InputNumber(self, current_Number: int) -> int:
        number = int(input("숫자를 입력하세요 : "))
        while self.__CheckPossibleNumber(current_Number, number) == False:
            number = int(input("제대로 된 숫자를 다시 입력하세요 : "))
        return number

    def __CheckPossibleNumber(self, current_Number: int, final_Number: int) -> bool:
        if current_Number < final_Number <= current_Number + 3:
            return True
        else:
            return False

    def __CheckGameOver(self, current_Number: int) -> bool:
        if current_Number >= 31:
            return True
        else:
            return False