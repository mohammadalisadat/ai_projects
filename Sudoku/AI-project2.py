import time


JADVAL = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
          [6, 0, 0, 1, 9, 5, 0, 0, 0],
          [0, 9, 8, 0, 0, 0, 0, 6, 0],
          [8, 0, 0, 0, 6, 0, 0, 0, 3],
          [4, 0, 0, 8, 0, 3, 0, 0, 1],
          [7, 0, 0, 0, 2, 0, 0, 0, 6],
          [0, 6, 0, 0, 0, 0, 2, 8, 0],
          [0, 0, 0, 4, 1, 9, 0, 0, 5],
          [0, 0, 0, 0, 8, 0, 0, 7, 9]]

class Sudoku:
    def __init__(self,jadval):
        self.jadval= [row[:] for row in jadval]
        self.marahel= 0
        self.namayeshmasir= False
        self.domains = {}
        self.reset_domains()

    def reset_domains(self):
            self.domains = {}
            for r in range(9):
                for c in range(9):
                    if self.jadval[r][c] == 0:
                        self.domains[(r, c)] = set(range(1, 10))
                    else:
                        self.domains[(r, c)] = {self.jadval[r][c]}
            for r in range(9):
                for c in range(9):
                    if self.jadval[r][c] != 0:
                        val = self.jadval[r][c]
                        self.checkforward(r, c, val)
    def printjadval(self):
        print("-" * 25)
        for i in range(9):
            row = "| "
            for j in range(9):
                val = self.jadval[i][j]
                row += str(val) if val != 0 else "."
                row += " "
                if (j + 1) % 3 == 0: row += "| "
            print(row)
            if (i + 1) % 3 == 0: print("-" * 25)
        
        if self.namayeshmasir:
            print(f"masir: {self.namayeshmasir}")
            time.sleep(0.02)

    def check(self, row, col, value):
        for c in range(9):
            if self.jadval[row][c] == value: return False
        for r in range(9):
            if self.jadval[r][col] == value: return False
        start_r, start_c = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_r, start_r + 3):
            for c in range(start_c, start_c + 3):
                if self.jadval[r][c] == value: return False
        return True

    def findempty(self):
        for i in range(9):
            for j in range(9):
                if self.jadval[i][j] == 0:
                    return (i, j)
        return None

    def backtracking(self):
        var = self.findempty()
        if not var:
            return True
        row, col = var
        for val in range(1, 10):
            if self.check(row, col, val):
                self.jadval[row][col] = val
                self.marahel += 1
                if self.namayeshmasir:
                    self.printjadval()

                if self.backtracking():
                    return True
                ##print("masir nadorost")
                self.jadval[row][col] = 0
                
        return False

    def varmrv(self):
        minvar = 10
        bestvar = None
        
        for i in range(9):
            for j in range(9):
                if self.jadval[i][j] == 0:
                    count = 0
                    for val in range(1, 10):
                        if self.check(i, j, val):
                            count += 1
                    
                    if count < minvar:
                        minvar = count
                        bestvar = (i, j)
                        if minvar == 1:
                            return bestvar
        return bestvar

    def mrv(self):
        var = self.varmrv()
        if not var:
            return True
        row, col = var
        
        for val in range(1, 10):
            if self.check(row, col, val):
                self.jadval[row][col] = val
                self.marahel += 1
                if self.namayeshmasir: self.printjadval()

                if self.mrv():
                    return True
                
                self.jadval[row][col] = 0
        return False


    def domain(self, row, col):
     domain = []
     for v in range(1, 10):
        if self.check(row, col, v):
            domain.append(v)
     return domain

    def checkforward(self, row, col, val):

        delete = []

        for (r, c) in self.hamsayeha(row, col):
            if val in self.domains[(r, c)]:
                self.domains[(r, c)].remove(val)
                delete.append((r, c, val))

                if len(self.domains[(r, c)]) == 0:
                    return False, delete

        return True, delete

    def backdomain(self, delete):
        for r, c, v in delete:
            self.domains[(r, c)].add(v)

    def hamsayeha(self, row, col):
        hamsayeha = set()
        for c in range(9):
            if c != col: hamsayeha.add((row, c))
        for r in range(9):
            if r != row: hamsayeha.add((r, col))
        br, bc = 3 * (row // 3), 3 * (col // 3)
        for r in range(br, br + 3):
            for c in range(bc, bc + 3):
                if (r, c) != (row, col): hamsayeha.add((r, c))
        return hamsayeha

    def forwardchecking(self):

        var = self.findempty()
        if not var:
            return True

        row, col = var

        domain = sorted(list(self.domains[(row, col)]))

        for value in domain:
            if self.check(row, col, value):

                self.jadval[row][col] = value
                self.marahel += 1

                if self.namayeshmasir:
                    self.printjadval()

                check, delete = self.checkforward(row, col, value)

                if check:
                    if self.forwardchecking():
                        return True

                self.backdomain(delete)
                self.jadval[row][col] = 0


        return False
def jadvaldasti():
    print("enter number  row:")
    jadval = []
    for i in range(9):
        while True:
            try:
                line = input(f"row {i+1}: ").split()
                row = [int(x) for x in line]
                if len(row) == 9:
                    jadval.append(row)
                    break
            except: pass
            print(" enter again")
    return jadval

def file():
    try:
        with open("sudoku.txt", "r") as f:
            jadval = [[int(n) for n in line.split()] for line in f if line.strip()]
        return jadval if len(jadval) == 9 else JADVAL
    except:
        return JADVAL


if __name__ == "__main__":
    while True:
        print("\nsudoku project")
        print("\nravesh vared kardan jadval:")

        print("1. dasti")
        print("2.default")
        print("3. file")
        mode = input(": ")
        
        jadval = []
        if mode == '1': jadval = jadvaldasti()
        elif mode == '3': jadval = file()
        else: jadval = JADVAL
        
        solver = Sudoku(jadval)
        print("JADVAL")
        solver.printjadval()
        
        print("\nsolve:")
        print("1. Backtracking")
        print("2. MRV")
        print("3. ForwardChecking ")
        
        option = input("enter your option: ")
        namayesh = input("namayesh masir?(y/n): ")
        if namayesh.lower() == 'y': solver.namayeshmasir = True
        
        start = time.time()
        solve = False
        
        if option == '1': solve = solver.backtracking()
        elif option == '2': solve = solver.mrv()
        elif option == '3': solve = solver.forwardchecking()
        
        end = time.time() - start
        
        if solve:
            print(f"\n time {end:.4f} ")
            print(f"marahel: {solver.marahel}")
            solver.printjadval()
        else:
            print("not solve")
            
        if input("exit (y/n): ") == 'y': break