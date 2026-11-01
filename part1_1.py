import hashlib
import time
import matplotlib.pyplot as plt

f = open("part1_1.csv", 'w')
f.write(",0,1,2,3,4,5,6,7,8,9,avg,total_trial\n")

class Block:
    def __init__(self,index, prev_hash, data, T):
        self.index=index
        self.prev_hash = prev_hash
        self.data = data
        self.nonce =0 
        self.hash = None
        self.target=T

    def encode(self) :
        return (
            f"{self.index}|{self.data}|{self.prev_hash.hex()}|{self.target}|{self.nonce}"
        ).encode('utf-8')


    def calNonce(self) :
        trial = 0
        while(True) :
            hashed_data = hashlib.sha256(self.encode())
            H = int.from_bytes(hashed_data.digest(), 'big')                 #해시를 unsinged 정수로 바꾸기
            trial+=1
            if(H < self.target) :
                self.hash = hashed_data.digest()
                break
            else:  
                self.nonce +=1
        return trial


    def calHash(self) :
        self.hash = hashlib.sha256(self.encode()).digest()
        return self.hash



def chainGen(n, T) :           #반복 횟수만큼 해시 체인 생성
    f.write(f"{T}")
    total_time = 0
    total_trial=0

    chain = []
    prev_hash = bytes(32);      #32byte의 0 저장

    for i in range(n):
        b = Block(i, prev_hash, i, T)

        start = time.perf_counter()
        total_trial += b.calNonce()
        end = time.perf_counter()


        elapsed_time = end - start
        total_time += elapsed_time
        avg = total_time/n
        print(f"{i} 번 실험 : {elapsed_time}\n")

        f.write(f",{elapsed_time}")

        prev_hash = b.hash
        chain.append(b)

    f.write(f",{avg},{total_trial}\n")
    
    return chain




x = [252, 248, 244, 240, 236]
for i in x:
    chainGen(10, 2**i)

f.close()
