#Jordan Page
#jpag513

class GameBoard:
    def __init__(self, size):
        self.size=size
        self.num_entries = [0] * size
        self.items = [[0] * size for i in range(size)]
        self.points = [0] *2
    def num_free_positions_in_column(self, column):
        return self.size - self.num_entries[column]
    def game_over(self):
        for i in self.num_entries:
            if i != self.size:
                return False
        return True
    def display(self):
        for i in range(self.size -1, -1, -1):
            for j in range(self.size):
                if self.items[j][i]== 0:
                    print(" ", end = " ")
                elif self.items[j][i] == 1:
                    print("o", end = " ")
                elif self.items[j][i] == 2:
                    print("x", end = " ")
            print()
        print("-" * (self.size + self.size - 1))
        for i in range(self.size):
            print(i, end = " ")
        print()
        print("Points player 1:", self.points[0])
        print("Points player 2:", self.points[1])
    
    def num_new_points(self, column, row, player):
        # horizontal points
        points = 0
        h_counter = 0
        for i in range(column - 3, column + 4):
            if i < 0 or i>= self.size:
                continue
            if self.items[i][row] == player:
                h_counter += 1
            elif self.items[i][row] != player:
                h_counter = 0
            if h_counter == 4:
                points +=1
                h_counter -= 1
                
        # vertical points
        v_counter = 0
        for j in range(row - 3, row + 4):
            if j < 0 or j >= self.size:
                continue
            if self.items[column][j] == player:
                v_counter += 1
            elif self.items[column][j]!= player:
                v_counter = 0
            if v_counter == 4:
                points += 1
                v_counter -= 1
                
        # diagonal points l-->r
        d_counter = 0
        test_col = [num for num in range(column - 3, column + 4)]        
        test_row = [num for num in range(row -3, row + 4)]
        for k in range(len(test_col)):
            if test_col[k] < 0 or test_row[k] < 0 or test_col[k] >= self.size or test_row[k] >= self.size:
                continue
            if self.items[test_col[k]] [test_row[k]] == player:
                d_counter += 1
            elif self.items[test_col[k]] [test_row[k]] != player:
                d_counter = 0
            if d_counter == 4:
                points += 1
                d_counter -= 1
        # diagonal points r-->l
        d_2_counter = 0
        test_col_2 = [num for num in range(column + 3, column - 4, -1)]        
        test_row_2 = [num for num in range(row -3, row + 4)]
        for l in range(len(test_col_2)):
            if test_col_2[l] < 0 or test_row_2[l] < 0 or test_col_2[l] >= self.size or test_row_2[l] >= self.size:
                continue
            if self.items[test_col_2[l]] [test_row_2[l]] == player:
                d_2_counter -= 1
            elif self.items[test_col_2[l]] [test_row_2[l]] == player:
                d_2_counter = 0
            if d_2_counter == -4:
                points += 1
                d_2_counter += 1
                      
        return points

    def add(self, column, player):
        if self.num_entries[column] >= self.size or column < 0 or column >= self.size:
            return False
        row = self.num_entries[column]
        self.items[column][row] = player 
        self.num_entries[column] += 1
        self.points[player - 1] += self.num_new_points(column, row, player)
        return True
    def free_slots_as_close_to_middle_as_possible(self):
        a_list = [i for i in range(self.size) if self.num_free_positions_in_column(i) != 0]
        mid = (0 + (self.size - 1)) / 2
        final_list = []
        for i in range(len(a_list)):
            lowest_index = 0
            for el in a_list:
                if abs(mid - el) < abs(mid - a_list[lowest_index]):
                    lowest_index = a_list.index(el)
                elif abs(mid - el) == abs(mid - a_list[lowest_index]):
                    lowest_index = min(el,lowest_index)
            final_list.append(a_list.pop(lowest_index))
        return final_list
                
    def column_resulting_in_max_points(self, player):
        highest_points = 0
        highest_col = self.free_slots_as_close_to_middle_as_possible()[0]
        for col in range(self.size):
            row = self.num_entries[col]
            if row < self.size:
                self.items[col][row] = player 
                points = self.num_new_points(col, row, player)
                if points > highest_points:
                    highest_points = points
                    highest_col = col
                elif points == highest_points:
                    min_index = min(self.free_slots_as_close_to_middle_as_possible().index(col),self.free_slots_as_close_to_middle_as_possible().index(highest_col))
                    highest_col = self.free_slots_as_close_to_middle_as_possible()[min_index]
                self.items[col][row] = 0 
        return highest_col, highest_points

                  
class FourInARow:
    def __init__(self, size):
        self.board=GameBoard(size)
    def play(self):
        print("*****************NEW GAME*****************")
        self.board.display()
        player_number=0
        print()
        while not self.board.game_over():
            print("Player ",player_number+1,": ")
            if player_number==0:
                valid_input = False
                while not valid_input:
                    try:
                        column = int(input("Please input slot: "))       
                    except ValueError:
                        print("Input must be an integer in the range 0 to ", self.board.size)
                    else:
                        if column<0 or column>=self.board.size:
                            print("Input must be an integer in the range 0 to ", self.board.size)
                        else:
                            if self.board.add(column, player_number+1):
                                valid_input = True
                            else:
                                print("Column ", column, "is alrady full. Please choose another one.")
            else:
                # Choose move which maximises new points for computer player
                (best_column, max_points)=self.board.column_resulting_in_max_points(2)
                if max_points>0:
                    column=best_column
                else:
                    # if no move adds new points choose move which minimises points opponent player gets
                    (best_column, max_points)=self.board.column_resulting_in_max_points(1)
                    if max_points>0:
                        column=best_column
                    else:
                        # if no opponent move creates new points then choose column as close to middle as possible
                        column = self.board.free_slots_as_close_to_middle_as_possible()[0]
                self.board.add(column, player_number+1)
                print("The AI chooses column ", column)
            self.board.display()   
            player_number=(player_number+1)%2
        if (self.board.points[0]>self.board.points[1]):
            print("Player 1 (circles) wins!")
        elif (self.board.points[0]<self.board.points[1]):    
            print("Player 2 (crosses) wins!")
        else:  
            print("It's a draw!")
            
game = FourInARow(6)
game.play()         
         
            


