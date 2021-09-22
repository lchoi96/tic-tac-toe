import numpy as np
import time
import warnings

m = 3
n = 3
k = 3

warnings.filterwarnings("ignore")


class prunedGame():
    # state count is a class variable used to count the number of states visited
    state_count = 0

    # initialise m,n,k
    def __init__(self, m=3, n=3, k=3):
        prunedGame.state_count = 0
        self.state = np.zeros([m, n])  # starting state
        if m < 1 or n < 1 or k < 1:
            raise ValueError('Unusable m,n,k')
        self.m = m
        self.n = n
        self.k = k

        # create a list of actions
        # each action is a m,n matrix with one entry set to 1, ie picking that cell
        # this is so we can add valid actions to a state to get the next state
        self.actions = []
        for i in range(self.m):
            for j in range(self.n):
                action = np.zeros([self.m, self.n])
                action[i, j] = 1
                self.actions.append(action)

    # max fn
    def max_val(self, state, a=-np.inf, b=np.inf):
        '''
        Max's value for a state
        '''
        # increase the number of states counted
        prunedGame.state_count += 1
        # terminal test

        terminal, utility = self.is_terminal(state)
        if terminal:
            return utility, None
        v = -np.inf
        final_action = []
        # for each action available
        for action in self.actions:

            # check if action is valid
            if self.is_valid(state, action):

                # since the valid cell is 0, we can just add +1/-1 to it
                new_val, act_temp = self.min_val(state + action, a, b)

                # if higher valued action found
                if v < new_val:

                    # create a new list of actions
                    v = new_val  # set v = max(v,new_val)
                    final_action = []
                    final_action.append(action)

                # action same value as before
                elif v == new_val:
                    # add to a list
                    if act_temp is not None:
                        final_action.append(action)

                if v >= b:
                    return v, None
                a = max(a, v)

        final_action = final_action[np.random.randint(len(final_action))]
        return v, final_action

    # min fn
    def min_val(self, state, a=-np.inf, b=np.inf):
        '''
        Min's value for a state
        '''
        # increase the number of states counted
        prunedGame.state_count += 1
        # terminal test

        terminal, utility = self.is_terminal(state)
        if terminal:
            return utility, None
        v = np.inf
        final_action = []
        # for each action available
        for action in self.actions:

            # check if action is valid
            if self.is_valid(state, action):
                new_val, act_temp = self.max_val(state + action * -1, a, b)

                # if lower valued action found
                if v > new_val:

                    # create a new list of actions
                    v = new_val  # set v = min(v,new_val)
                    final_action = []
                    final_action.append(action)

                # action same value as before
                elif new_val == v:
                    # add to a list
                    if act_temp is not None:
                        final_action.append(action)

                if v <= a:
                    return v, None
                b = min(b, v)

        final_action = final_action[np.random.randint(len(final_action))]
        return v, final_action

    def input_to_action(self, string):
        '''
        Converts string input to an action
        '''
        action = np.zeros([self.m, self.n])
        string = string.split()
        try:
            x = int(string[0]) - 1
            y = int(string[1]) - 1
        except:
            print('Input not recognised, please try again in the format X Y')
            raise ValueError

        action[x, y] = 1
        return action

    def is_terminal(self, state):
        '''
        Function returns a boolean for whether it is terminal and a value for the utility
        Eg if X wins, return 1 or if O wins, return -1

        Arguments:
        state - an array that represents the state of the board, with max's positions as 1's,
        min's positions as -1's, and empty cells as 0's.
        '''
        # create the board, with max's moves denoted with X
        # and min's moves denoted with O
        array_board = np.empty([self.m, self.n], dtype=object)
        array_board[state == 1] = 'X'
        array_board[state == 0] = ' '
        array_board[state == -1] = 'O'

        # what each player needs to get to win
        max_string = 'X' * self.k
        min_string = 'O' * self.k

        # check in the horizontal direction
        for i in array_board:
            row = i.tolist()
            joined = ''.join(row)
            if max_string in joined:
                return True, 1
            elif min_string in joined:
                return True, -1
        # check in the vertical direction
        for i in array_board.T:
            row = i.tolist()
            joined = ''.join(row)
            if max_string in joined:
                return True, 1
            elif min_string in joined:
                return True, -1

        # check in the diagonal direction
        diags = [array_board.diagonal(i) for i in
                 range(array_board.shape[1] - 1, -array_board.shape[0], -1)]
        diags.extend(np.fliplr(array_board).diagonal(i) for i in
                     range(array_board.shape[1] - 1, -array_board.shape[0],
                           -1))
        # remove diagonals less than k
        diags_filtered = [d for d in diags if len(d) >= self.k]

        for diagonal in diags_filtered:
            diagonal = diagonal.tolist()
            joined = ''.join(diagonal)
            if max_string in joined:
                return True, 1
            elif min_string in joined:
                return True, -1

        # check if there are any empty spaces left
        # if there aren't, then the game is over, and they've tied
        if ' ' not in array_board:
            return True, 0
        return False, 0

    def is_valid(self, state, action):
        '''
        Function that takes in a state and action and checks if valid
        '''

        # obtains the coordinates of said action
        coord_x, coord_y = self.action_to_coord(action)

        # checks if the current coordinate on the map is 0, ie it has not been played yet
        if state[coord_x, coord_y] != 0:
            return False
        return True

    def action_to_coord(self, action):
        '''
        An action is a m,n matrix of zeros with entry of 1 (or -1)
        Returns the coordinates of this action
        '''
        c = np.where(action != 0)
        return c[0][0], c[1][0]

    def drawboard(self):
        '''
        Draws the current board
        '''
        # create the board, with max's moves denoted with X
        # and min's moves denoted with O
        board = np.empty([self.m, self.n], dtype=object)
        board[self.state == 1] = 'X'
        board[self.state == 0] = ' '
        board[self.state == -1] = 'O'

        list_lines = []
        # returns the range of n
        labels = [str(code) for code in range(1, self.n + 1)]
        top_line = ' ' * 4 + (' ' * 3).join(labels) + '\n'
        # for each row of m, create column dividers
        for index, row_line in enumerate(board):
            list_lines.append(
                str(index + 1) + ' | ' + ' | '.join(row_line) + ' |\n')
        # row borders
        line_border = '  ' + '-' * 4 * self.n + '-\n'

        board_str = top_line + line_border + line_border.join(
            list_lines) + line_border
        print(board_str)

    def initialise_game(self):
        '''
        Function to start the game
        '''
        self.state = np.zeros([self.m, self.n])
        print('New game')
        print('To pick a cell, input a string in the format X Y')
        print('X goes from 1 to ' + str(self.m) + ', Y goes from 1 to ' + str(
            self.n))
        while not self.is_terminal(self.state)[0]:
            self.drawboard()
            print('New turn')

            # max plays
            while True:

                _, max_action = self.max_val(self.state)
                coord = self.action_to_coord(max_action)
                print('We recommend using:', coord[0] + 1, coord[1] + 1)
                action = input(
                    'Please input which cell to pick in the format X Y, or 1 1\n ')
                try:
                    action = self.input_to_action(action)
                except:
                    continue
                # if the action is valid
                if self.is_valid(self.state, action):
                    self.state += action

                    self.drawboard()
                    break

                else:
                    print('Action invalid, please try again')

            if self.is_terminal(self.state)[0]:
                break
                # min plays
            _, min_action = self.min_val(self.state)
            self.state += min_action * -1
            print('Min plays')
            if self.is_terminal(self.state)[0]:
                self.drawboard()
                break

        winner = self.is_terminal(self.state)[1]
        if winner == 1:
            print('Max wins!')
        elif winner == -1:
            print('Min wins')
        else:
            print('Draw')
        print('Game over!')

# code to time the max function for various m,n,k from 1-3
# it prints out time taken and number of states visited
def print_complexity(ret=False, printout=True):
    print('m, n, k, time, states')
    time_taken_pruned = np.zeros([3, 3, 3])
    space_taken_pruned = np.zeros([3, 3, 3])
    for m in range(1, 4):  # 1-3
        for n in range(1, 4):
            for k in range(1, max(m, n) + 1):
                start = time.time()
                prunedGame.state_count = 0
                pgame = prunedGame(m=m, n=n, k=k)
                pgame.max_val(np.zeros([m, n]))
                end = time.time()
                time_taken_pruned[m - 1, n - 1, k - 1] = end - start
                space_taken_pruned[m - 1, n - 1, k - 1] = pgame.state_count
                if printout:
                    print(m, n, k, end - start, pgame.state_count)
    if ret:
        return time_taken_pruned, space_taken_pruned


# dividing the time taken to run max without pruning by the time taken to run max with pruning
def print_difference():
    import game as g
    print('\nAnalysing the effect of pruning... \n')
    print('Time taken, states visited without pruning')
    t, s = g.print_complexity(ret=True, printout=True)
    print('\nTime taken, states visited with pruning')
    t_p, s_p = print_complexity(ret=True, printout=True)
    time_diff = t / t_p
    states_diff = s / s_p
    time_diff = np.transpose(time_diff, (2, 0, 1))
    states_diff = np.transpose(states_diff, (2, 0, 1))
    print('\nNow we divide the time taken without pruning by the time taking '
          'with pruning')
    print(
        '\nFor the next part, nan may occur due to the division in the '
        'time/number of states in games where the game is not ran as k > max(m, n)')
    print(
        'Also note that division here is approximate due to rounding errors '
        'in python\n')
    print('\nChange in time taken for k=1,2,3 respectively')
    
    print(time_diff)
    print('\nChange in number of states for k=1,2,3 respectively')
    print(states_diff)


if __name__ == "__main__":
    game = prunedGame(m=3, n=3, k=3)
    game.initialise_game()
    print('To play again please run the script again\n')
    print_difference()
    print('\nThank you!')
