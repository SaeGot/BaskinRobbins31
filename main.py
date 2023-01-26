import BaskinRobbins31 as BR31
import QLearning as QL


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    ql = QL.QLearning()
    q_table = ql.GetQTable("BaskinRobbins31_Q.csv")

    br31 = BR31.BaskinRobbins31()
    br31.StartGame(False)

