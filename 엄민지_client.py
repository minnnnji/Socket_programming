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
    for i in range(0, 3):
        while ((num in answer) | (num in except_num)) : 
            num = random.randrange(1,10)
        answer.append(num)

    return answer
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
def count_SB(answer,guess):
    cnt = [0,0]
    for i in range(0,3):
        for j in range(0,3):
            if ((answer[j] == guess[i]) & (i == j)):
                cnt[0] += 1
            if ((answer[j] == guess[i]) & (i != j)):
                cnt[1] += 1
    return cnt

from socket import *
import random

to = 'To Server:'
fr = 'From Server:'
request = 'request_game'

to_strike = 0
to_ball = 0
fr_strike = 0
fr_ball = 0

except_num = []
answer = [] 
guess = []
done_digit = []
receive_ans = [] 
# 여기서부터는 정답 digit 만들기
answer = make_digit(except_num)
guess = make_digit(except_num)

to_score = [to_strike ,to_ball]
fr_score = [fr_strike ,fr_ball]

serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(('localhost',serverPort))


ans = input('Do you want to play a game? (Yes or No) '); 
if(ans =='No'):

    clientSocket.send(ans.encode('utf-8'))
    clientSocket.close()

elif(ans == 'Yes'):

    print(to , request) # 요청하기 
    clientSocket.send(request.encode('utf-8')) # 요청 보내기

    data = clientSocket.recv(1024) 
    print(fr , data.decode('utf-8')) # 확인 받고 프린트

    print('Answer:',answer[0] * 100 + answer[1] * 10 + answer[2])
    k = 0
    cnt = 0
    #정답 프린트
    while(1):
        cnt += 1
        
        if(fr_score[1]==3):
            done_digit,guess = digit_3ball(done_digit,guess)
            guess_num = make_msg(guess,to_score)
        else:
            guess = make_digit(except_num)
            guess_num = make_msg(guess,to_score)
        #print(cnt,answer,'\n')
        print(to+guess_num)
        clientSocket.send(guess_num.encode('utf-8')) 

        data = clientSocket.recv(1024).decode('utf-8')
        print(fr+data)

        receive_ans,fr_score = make_int(data)
        to_score = count_SB(answer,receive_ans)

        if ((fr_score[0] == 0) & (fr_score[1] == 0)&(cnt != 1)):
            for i in range(0,3):
                except_num.append(guess[i])
            #print(except_num)
        if ((fr_score[0]==3)&(to_score[0]==3)):
            print('Draw!')
            msg = make_msg(guess,to_score)
            print(to+msg)
            clientSocket.send(msg.encode('utf-8')) 
            k = 1 
        elif(fr_score[0] == 3):
            print('Client Win!')
            msg = make_msg(guess,to_score)
            print(to+msg)
            clientSocket.send(msg.encode('utf-8')) 
            k = 1
        elif(to_score[0] == 3):
            print('Client Lose!')
            guess = [0,0,0]
            msg = make_msg(guess,to_score)
            print(to+msg)
            clientSocket.send(msg.encode('utf-8'))
            k = 1

        if k == 1:
            break
clientSocket.close()