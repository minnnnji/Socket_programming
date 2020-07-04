from itertools import combinations

def make_msg(num,score):
    num = list(map(str,num))
    score = list(map(str,score))

    msg = str('['+num[0]+', '+num[1]+', '+num[2]+']/['+score[0]+', '+score[1]+']')
    return msg
def make_int(receive):
    result = []
    score = []
    cnt = 0
    for i in range(len(receive)):
        if (((receive[i]>='0')&(receive[i]<='9')&(cnt<3))):
            result.append(int(receive[i]))
            cnt += 1
        elif((receive[i]>='0')&(receive[i]<='9')):
            score.append(int(receive[i]))
            cnt += 1

    return result,score

def make_digit(except_num):
    answer = []
    num = random.randrange(1,10)
# = [i for i in b if i not in a]
    for i in range(0,3):
        while ((num in answer) | (num in except_num)) : 
            num = random.randrange(1,10)
        answer.append(num)

    return answer

def count_SB(answer,guess):
    cnt = [0,0]
    for i in range(0,3):
        for j in range(0,3):
            if ((answer[j] == guess[i]) & (i == j)):
                cnt[0] += 1
            if ((answer[j] == guess[i]) & (i != j)):
                cnt[1] += 1
    return cnt
def digit_3ball(done_digit,original):
    done_digit.append(original)
    for i in range(0,len(done_digit)):
        k = check_3ball_digit(done_digit[i])
        if(k==1):
            continue
        else:
            return done_digit,k
    return done_digit,make_3ball_digit(original)
def make_3ball_digit(original):
    random.shuffle(original)
    return original
def check_3ball_digit(original):
    result = []
    result = make_3ball_digit(original)
    if result == original:
        return 1
    else:
        return result

from socket import *
import random

fr = 'From Client:'
to = 'To Client:'

to_strike = 0
to_ball = 0
fr_strike = 0
fr_ball = 0

answer = [] 
guess = []
except_num = []
done_digit = []

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('localhost', serverPort))
serverSocket.listen(1)


to_score = [to_strike ,to_ball]
fr_score = [fr_strike ,fr_ball]
# 여기서부터는 정답 digit 만들기
answer = make_digit(except_num)
guess = make_digit(except_num)

print('The server is ready to receive a game request')
client_socket, addr = serverSocket.accept()

data = client_socket.recv(1024).decode('utf-8')

k = 0
cnt = 0 

#게임을 원하는지 안원하는지 부터 받기
if(data == 'No'):
    serverSocket.close()
else:
    print(fr,data) 
    print(to,'ok')
    client_socket.send('ok'.encode('utf-8'))
    print('Answer:',answer[0] * 100 + answer[1] * 10 + answer[2])

    #여기 까지 완전 처음 부분 정답 미리 말해주기
    while(1):
        cnt += 1
        data = client_socket.recv(1024).decode()
        #print(cnt,answer,'\n')
        print(fr,data)

        receive_ans,fr_score = make_int(data)
        to_score = count_SB(answer,receive_ans)

        if((fr_score[0] == 0) & (fr_score[1] == 0)&(cnt != 1 )):
            for i in range(0,3):
                except_num.append(guess[i])
            #print(except_num)
        if(fr_score[0]==3):
            print('Server Win!')
            guess = [0,0,0]
            msg = make_msg(guess,to_score)
            client_socket.send(msg.encode('utf-8'))
            break
        #print(fr_score)
        if(fr_score[1]==3):
            done_digit,guess = digit_3ball(done_digit,guess)
            guess_num = make_msg(guess,to_score)
        else:
            guess = make_digit(except_num)
            guess_num = make_msg(guess,to_score)

        if(fr_score[0]!=3):
            print(to+guess_num)
            client_socket.send(guess_num.encode('utf-8'))

        if ((fr_score[0]==3)&(to_score[0]==3)):

            print('Draw!')
            k = 1 
        elif(to_score[0] == 3):
            data = client_socket.recv(1024).decode()
            print(fr,data)

            print('Server Lose!')

            guess_num =make_msg(guess,to_score)
            client_socket.send(guess_num.encode('utf-8'))
            data = client_socket.recv(1024).decode()
            k = 1
        if k == 1:
            break    
    
    serverSocket.close()
    # '''