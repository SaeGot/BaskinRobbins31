import csv
import random


class QLearning:
    def __init__(self):
        self.qTable = QTable()
        self.sarsList = []  #(state, action, reward, next_state)

    def Initialize(self, file_Name: str, init_QValue: bool=False):
        '''
        Q-Learning 초기화

        :param file_Name: Q 테이블 CSV 파일명
        :param init_QValue: 모든 Q값 초기화 여부
        '''
        f = open(file_Name, "r")
        csv_r = csv.reader(f)

        self.qTable.table = {}
        action_line = True
        self.qTable.stateCount = 0
        for line in csv_r:
            if action_line == True:
                action_line = False
                self.__InitializeActionList(line)
            else:
                self.__InitializeQTable(line, init_QValue)

        f.close()

    def Learn(self, starting_State: str, end_State: str, is_FirstPlayer: bool, winning_Reward: float,
              learning_Rate: float, discount_Factor: float, epsilon_Greedy: float):
        '''
        학습

        :param starting_State: 시작 상태
        :param end_State: 에피소드 종료 상태
        :param is_FirstPlayer: 학습대상이 첫 턴
        :param winning_Reward: 승리시 보상 값
        :param learning_Rate: 학습률
        :param discount_Factor: 할인율
        :param epsilon_Greedy: 입실론-그리디 값
        '''
        epsilon_greedy = max(0.0, min(epsilon_Greedy, 1.0))
        self.sarsList = []
        current_num = starting_State
        action = ""
        current_state = starting_State
        is_player_turn = is_FirstPlayer
        while current_num != end_State:
            if is_player_turn:
                action = self.__GetAction(current_num, epsilon_greedy)
                current_num = self.__GetNextNumber(current_num, action)
                is_player_turn = not is_player_turn
            else:
                selected_num = self.__GetAction(current_num, epsilon_greedy, True)
                next_state = self.__GetNextNumber(current_num, selected_num)
                if next_state == end_State:
                    reward = winning_Reward
                else:
                    reward = 0
                if action != "":
                    self.__SetSARS(current_state, action, next_state, is_player_turn, reward)
                    self.__UpdateQValue(current_state, next_state, action, reward, learning_Rate, discount_Factor)
                is_player_turn = not is_player_turn
                current_num = next_state
                current_state = next_state

    def WriteQTable(self, file_Name: str):
        '''
        Q 테이블 쓰기

        :param file_Name: Q 테이블 CSV 파일명
        '''
        f = open(file_Name, 'w', newline='')
        wr = csv.writer(f)
        line = [""]
        for action in self.qTable.actionList:
            line.append(action)
        wr.writerow(line)
        for state in self.qTable.stateList:
            line = [state]
            for action in self.qTable.actionList:
                line.append(str(self.qTable.GetQValue(state, action)))
            wr.writerow(line)

    def GetBestAction(self, current_State: str) -> str:
        '''
        최적 행동 가져오기

        :param current_State: 현재 상태
        :return: 행동
        '''
        action = self.qTable.actionList[0]
        max_q = self.qTable.GetQValue(current_State, self.qTable.actionList[0])
        for n in range(1, len(self.qTable.actionList)):
            q_value = self.qTable.GetQValue(current_State, self.qTable.actionList[n])
            if q_value > max_q:
                action = self.qTable.actionList[n]
                max_q = q_value

        return action

    def __InitializeActionList(self, line: []):
        '''
        행동 리스트 초기화

        :param line: csv의 첫 번째 라인
        '''
        self.qTable.actionCount = len(line) - 1
        self.qTable.actionList = []
        is_first_value = True
        for value in line:
            if is_first_value == True:
                is_first_value = False
            else:
                self.qTable.actionList.append(value)

    def __InitializeQTable(self, line: [], init_QValue: bool):
        '''
        QTable 초기화, 상태 리스트 초기화
        
        :param line: csv의 첫 번째 라인
        :param init_QValue: Q 값 초기화 여부
        '''
        self.qTable.stateCount += 1
        # 수치 설정
        value_list = []
        is_first_value = True
        first_value = ""
        n = 0
        for value in line:
            if is_first_value == True:
                is_first_value = False
                first_value = value
            else:
                if init_QValue:
                    self.qTable.table[(first_value, self.qTable.actionList[n])] = 0.0
                else:
                    self.qTable.table[(first_value, self.qTable.actionList[n])] = float(value)
                n += 1
        self.qTable.stateList.append(first_value)

    def __GetAction(self, current_State: str, epsilon_Greedy: float, random_Action: bool = False) -> str:
        '''
        행동 가져오기

        :param current_State: 현재 상태
        :param epsilon_Greedy: 입실론 그리디 값
        :return: 행동
        '''
        action = ""
        epsilon_greedy = epsilon_Greedy
        random_num = random.uniform(0, 1)
        if random_Action:
            epsilon_greedy = 1
        # 탐욕 행동
        if random_num > epsilon_greedy:
            action = self.GetBestAction(current_State)
        # 랜덤 행동
        else:
            index = random.randint(0, len(self.qTable.actionList) - 1)
            action = self.qTable.actionList[index]

        return action

    def __GetNextNumber(self, current_State: str, action: str) -> str:
        '''
        다음 숫자 가져오기

        :param current_State: 현재 상태
        :param action: 행동
        :return: 다음 숫자
        '''
        next_state = ""
        if int(current_State) + int(action) > 31:
            next_state = "31"
        else:
            next_state = str(int(current_State) + int(action))

        return next_state

    def __SetSARS(self, current_State: str, action: str, next_State: str, is_PlayerTurn: bool, reward: float):
        '''
        SARS 설정
        
        :param current_State: 현재 상태
        :param action: 행동
        :param is_PlayerTurn: 현재가 플레이어 턴
        :param reward: 보상값
        '''
        if int(next_State) > 31:
            next_state = "31"
        self.sarsList.append((current_State, action, reward, next_State))

    def __UpdateQValue(self, current_State: str, next_State: str, action: str, reward: float,
                       learning_Rate: float, discount_Factor: float):
        '''
        Q 값 업데이트
        
        :param current_State: 현재 상태
        :param next_State: 다음 상태
        :param action: 행동
        :param reward: 보상
        :param learning_Rate: 학습률
        :param discount_Factor: 감가율
        :return: 
        '''
        max_q = self.__GetMaxQValue(next_State)
        q_value = self.qTable.GetQValue(current_State, action)
        q_value = (1 - learning_Rate) * q_value \
                  + learning_Rate * (reward + discount_Factor * max_q)

        self.qTable.SetQValue(current_State, action, q_value)

    def __GetMaxQValue(self, current_State: str) -> float:
        '''
        최대 Q 값 가져오기

        :param current_State: 현재 상태
        :return: 최대 Q 값
        '''
        max_q = self.qTable.GetQValue(current_State, self.qTable.actionList[0])
        for n in range(1, len(self.qTable.actionList)):
            q_value = self.qTable.GetQValue(current_State, self.qTable.actionList[n])
            if q_value > max_q:
                max_q = q_value

        return max_q


class QTable:
    def __init__(self):
        self.stateCount = 0
        self.actionCount = 0
        self.actionList = []
        self.stateList = []
        self.table = {} #key : (state, action), value : qValue

    def GetQValue(self, state: str, action: str) -> float:
        '''
        Q값 가져오기

        :param state: 상태
        :param action: 행동
        :return: Q 값
        '''
        return self.table[(state, action)]

    def SetQValue(self, state: str, action: str, value: float):
        '''
        Q 값 설정

        :param state: 상태
        :param action: 행동
        :param value: Q 값
        '''
        self.table[(state, action)] = value
