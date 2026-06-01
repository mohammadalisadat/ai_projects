لهimport time
import random
import heapq
import collections


END= (1, 2, 3,  4,  5, 6, 7, 8, 0)
START = (7, 2, 4, 5,  0, 6, 8 ,  3,  1)

def printstate(state):
    print("-" * 13)
    for i in range(0, 9, 3):
        print(f"|{state[i]}|{state[i + 1]}|{state[i + 2]}|")
        print("-" * 13)


def hamsayeha(state):

    hamsayeha = []
    zerostate = state.index(0)
    row, col = zerostate // 3, zerostate % 3
    
    moves = [(-1, 0, 'up'), (1, 0, 'down'), (0, -1, 'left'), (0, 1, 'right')]

    for dr, dc, movename in moves:
        newrow, newcol = row + dr, col + dc
        
        if 0 <= newrow < 3 and 0 <= newcol < 3:
            newidx = newrow * 3 + newcol
            
            new = list(state)
            new[zerostate], new[newidx] = new[newidx], new[zerostate]
            
            hamsayeha.append((tuple(new), movename))
            
    return hamsayeha

def manhatan(state):

    d = 0
    for i in range(9):
        val = state[i]
        if val != 0:
            currentrow, currentcol = i // 3, i % 3

            endstate= val - 1
            endrow, endcol = endstate // 3, endstate % 3
            
            d += abs(currentrow - endrow) + abs(currentcol - endcol)
    return d


def bfs(state):
    starttime = time.time()
    queue = collections.deque([(state, [])])
    visit= set([state])
    nodes = 0

    while queue:
        currentstate, masir = queue.popleft()
        nodes+= 1

        if currentstate == END:
            finishtime = time.time() - starttime
            return masir, nodes, finishtime

        for hamsaye, move in hamsayeha(currentstate):
            if hamsaye not in visit:
                visit.add(hamsaye)
                queue.append((hamsaye, masir + [move]))

    return None, nodes, time.time() - starttime


def ids(state):
    starttime = time.time()
    
    def dls(state, masir, d, limit, visit):
        if state == END:
            return masir
        if d >= limit:
            return None
        
        for hamsaye, move in hamsayeha(state):
            if hamsaye not in visit:
                visit.add(hamsaye)
                result = dls(hamsaye, masir + [move], d + 1, limit, visit)
                if result is not None:
                    return result
                visit.remove(hamsaye)
        return None

    limit = 0
    nodes = 0
    while True:
        if time.time() - starttime > 30:
            print("(IDS Time Limit).")
            return None, nodes, time.time() - starttime
            
        visit= set([state])
        result = dls(state, [], 0, limit, visit)
        nodes += limit
        
        if result is not None:
            return result, nodes, time.time() - starttime
        limit += 1

def astar(state):
    starttime = time.time()
    queue = []
    h =manhatan(state)
    heapq.heappush(queue, (h, 0, state, []))
    
    visit = set()
    nodes = 0
    
    while queue:
        f, g, currentstate, masir = heapq.heappop(queue)
        
        if currentstate in visit:
            continue
        visit.add(currentstate)
        nodes+= 1
        
        if currentstate == END:
            return masir, nodes, time.time() - starttime
        
        for hamsaye, move in hamsayeha(currentstate):
            if hamsaye not in visit:
                newg = g + 1
                newh = manhatan(hamsaye)
                newf = newg + newh
                heapq.heappush(queue, (newf, newg, hamsaye, masir + [move]))
                
    return None, nodes, time.time() - starttime


def dasti():
    print("\nplease enter number 1-8 and 0 is empty")
    print("example: 7 2 4 5 0 6 8 3 1")
    try:
        raw = input("enter number with space ").strip().split()
        if len(raw) != 9:
            raise ValueError("incorect")
        state = tuple(map(int, raw))
        if sorted(state) != list(range(9)):
            raise ValueError("incorect")
        return state
    except Exception as e:
        print(e)
        return None

def randompuzzle():
    try:
        change = int(input("enter number of change : "))
    except:
        change = 10
        
    current = END
    for i in range(change):
        hamsaye= hamsayeha(current)
        current, i = random.choice(hamsaye)
    return current

def main():
    while True:
        print("\n" + "="*40)
        print("puzzle8 project")
        print("="*40)
        print("1.default ")
        print("2.dasti")
        print("3.random")
        print("4.exit")
        
        choice = input("enter number your  ")
        
        state = None
        
        if choice == '1':
            state = START
        elif choice == '2':
            state = dasti()
        elif choice == '3':
            state = randompuzzle()
        elif choice == '4':
            print("EXIT!")
            break
        else:
            print("incorect choice")
            continue
            
        if state:
            print("\nstart puzzle")
            printstate(state)
            
            print("1. A* ")
            print("2. BFS ")
            print("3. IDS ")
            
            choice = input("choice? ")
            masir = None
            nodes = 0
            finishtime = 0
            choicename = ""
            
            
            if choice == '1':
                choicename = "A*"
                masir, nodes, finishtime = astar(state)
            elif choice == '2':
                choicename = "BFS"
                masir, nodes, finishtime =bfs(state)
            elif choice == '3':
                choicename = "IDS"
                masir, nodes, finishtime= ids(state)
            else:
                print("incorect choice")
                continue
                

            if masir is not None:
                print(f"\n result :{choicename} ---")
                print(f" marahel:{len(masir)}")
                print(f"time : {finishtime:.6f} ")
                print(f"nudes: {nodes}")
                print(f" masir: {masir}")
                
                bool = input("\n namayesh masir(y/n): ")
                if bool.lower() == 'y':
                    curr = state
                    printstate(curr)
                    for idx, move in enumerate(masir):
                        print(f"\n marhale {idx+1}: move {move}")
                        for  hamsaye, movename in hamsayeha(curr):
                            if movename == move:
                                curr = hamsaye
                                break
                        printstate(curr)
            else:
                print("time has been over")

if __name__ == "__main__":
    main()
