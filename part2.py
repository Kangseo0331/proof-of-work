import hashlib
import time
import copy

f = open("part3.csv", 'w')
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
        self.nonce=0
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
        b = Block(i+1, prev_hash, i, T)

        start = time.perf_counter()
        total_trial += b.calNonce()
        end = time.perf_counter()


        elapsed_time = end - start
        total_time += elapsed_time
        avg = total_time/n
        print(f"block {i+1} : {elapsed_time}\n")

        f.write(f",{elapsed_time}")

        prev_hash = b.hash
        chain.append(b)

    f.write(f",{avg},{total_trial}\n")
    
    return chain



def verifier(chain, T):

    for i in range(len(chain)):
        b = chain[i]

        #블록 번호 검증
        if (b.index != i+1) : return False


        #고정 목표값 검증
        if(b.target != T): return False

        #재계산한 해시 검증
        recomputeHash = hashlib.sha256(b.encode()).digest()
        if(b.hash != recomputeHash) : return False

        #PoW 조건 검증
        H = int.from_bytes(recomputeHash, 'big')
        if(H >= b.target) : return False

        #이전 블록과의 해시 연결 확인
        if i == 0:
            if b.prev_hash != bytes(32):    #첫 번째 블록 32바이트 0인지 검사
                return False
        else:
            if b.prev_hash != chain[i - 1].hash:    #나머지 블록은 직전 블록의 hash와 일치하는지 확인
                return False

    return True


T_star = 2433849096262126601305031626558662622707783392882157128131455873201182
#T_star = 2**252



original = chainGen(10, T_star)
print("Original chain:", verifier(original, T_star))


copied = copy.deepcopy(original)
print("Copied chain(before chainging):", verifier(copied, T_star))
print("\n")






print("\n[recalculate from block 6]\n\n")


f.write(f"{T_star},,,,,")
total_time = 0
total_trial=0


copied[5].data = "change the block"
print("Copied chain(after chainging):", verifier(copied, T_star))
print("\n")

total_trial = 0
total_time = 0

start6 = time.perf_counter()
total_trial += copied[5].calNonce()
end6 = time.perf_counter()
elapsed_time6 = end6-start6
print(f"block 6: {elapsed_time6}\n")
f.write(f",{elapsed_time6}")

total_time += elapsed_time6

for i in range(6, 10):
    b = copied[i]
    b.prev_hash = copied[i-1].hash

    start = time.perf_counter()
    total_trial += b.calNonce()
    end = time.perf_counter()


    elapsed_time = end - start
    total_time += elapsed_time
    avg = total_time/5
    print(f"block {i+1}: {elapsed_time}\n")

    f.write(f",{elapsed_time}")

    prev_hash = b.hash


f.write(f",{avg},{total_trial}\n")


print("Copied chain(after repair):", verifier(copied, T_star))
print("\n")


f.close()
