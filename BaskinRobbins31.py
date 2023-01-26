import random
import QLearning

class BaskinRobbins31:
    def StartGame(self, player_First: bool=True):
        print("게임 시작합니다.")
        current_number = 0
        player_turn = player_First

        if player_First == False:
            # 상대 턴
            player_turn = False
            current_number = self.__GetRandomNumber(current_number)
            print(current_number)

        while True:
            # 플레이어 턴
            player_turn = True
            current_number = self.__InputNumber(current_number)
            if self.__CheckGameOver(current_number) == True:
                break
            # 상대 턴
            player_turn = False
            current_number = self.__GetRandomNumber(current_number)
            print(current_number)
            if self.__CheckGameOver(current_number) == True:
                break

        if player_turn == False:
            print("승리")
        else:
            print("패배")

    def StartLearning(self, epoch: int):
        n = 0
        while n >= epoch:
            current_number = 0

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