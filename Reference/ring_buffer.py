# 실시간 데이터처리를 위한 Ring Buffer(고정길이 큐, FixedQueue) 구현
import websockets
import asyncio
import json
from typing import Any
import matplotlib.pyplot as plt

class RingBuffer:
    class Empty(Exception):
        '''
        비어있는 RingBuffer에서 디큐 또는 피크할 떄 내보내는 예외 처리
        '''
        pass
    class Full(Exception):
        '''
        가득 차 있는 RiongBuffer에서 인큐할 때 내보내는 예외 처리
        '''
        pass

    def __init__(self, capacity:int)->None:
        '''초기화'''
        self.no=0 # 현재 데이터 개수
        self.front=0 # 맨 앞 원소 커서
        self.rear=0  # 맨 끝 원소 커서
        self.capacity=capacity # 큐 크기
        self.que=[None]*capacity # 큐 본체

    def __len__(self)->int:
        '''큐에 있는 데이터의 개수 반환'''
        return self.no

    def is_empty(self)->bool:
        '''큐가 비어있는지 판단'''
        return self.no<=0

    def is_full(self)->bool:
        '''큐가 비어있는지 판단'''
        return self.no>=self.capacity

    def enque(self, x:Any)->None:
        '''데이터 x를 인큐'''
        if self.is_full():
            raise RingBuffer.Full # 큐가 가득 차 있는 경우 예외 처리
        self.que[self.rear]=x
        self.rear+=1
        self.no+=1
        if self.rear==self.capacity:
            self.rear=0

    def deque(self)->Any: # 큐의 맨 앞부터 데이터를 디큐한다.
        '''데이터를 디큐'''
        if self.is_empty():
            raise RingBuffer.Empty # 큐거가 비어있는 경우 예외 처리
        x=self.que[self.front]
        self.front+=1
        self.no-=1

        if self.front==self.capacity:
            self.front=0
        return x

    def peek(self)->Any:
        '''큐에서 데이터를 피크(맨 앞 데이터를 들여다봄)'''
        if self.is_empty():
            raise RingBuffer.Empty # 큐가 비어있는 경우 예외 처리

        return self.que[self.front]

    def find(self,value:Any)->Any:
        '''큐에서 value를 찾아 인덱스를 반환, 없으면 -1 반환'''
        for i in range(self.no):
            idx=(i+self.front)%self.capacity

            if self.que[idx]==value:
                return idx

        return -1 # 검색 실패

    def count(self,value:Any)->bool:
        '''큐에 있는 value의 개수를 반환'''
        c=0
        for i in range(self.no): # 큐 데이터를 선형 검색
            idx = (i + self.front) % self.capacity
            if self.que[idx]==value:
                c+=1
        return c

    def __contains__(self, value:Any)->bool:
        '''큐에 value가 있는지 판단'''
        return self.count(value)

    def clear(self)->None:
        '''큐의 모든 데이터를 지움'''
        self.no=0
        self.front=0
        self.rear=0

    def dump(self)->None:
        '''모든 데이터를 맨 앞부터 맨 끝 순으로 출력'''
        is_printMode=True # print만할지 return할지 결정

        if self.is_empty():
            print("Queue is Empty!")
        else:
            if is_printMode==True:
                for i in range(self.no):
                    print(self.que[(i+self.front)%self.capacity], end='')
                print()
            else:
                pass

    def plot_single_graph(self):
        # range setting
        if self.is_full():
            y_item =self.que[0:]
        else:
            if self.front<=self.rear:
                y_item=self.que[self.front:self.rear+1]
            else:
                y_item = self.que[self.front:]+self.que[0:self.rear+1]

        print("y item" , y_item)
        plt.plot(y_item)
        plt.ylabel('test_graph')
        plt.show()

async def upbit_ws_client(ring_buffer:RingBuffer):
    uri = "wss://api.upbit.com/websocket/v1"

    async with websockets.connect(uri,  ping_interval=60) as websocket:
        subscribe_fmt = [
            # Ticket Field
            {
                "ticket":"test"
            },

            # Type Field
            {
                "type": "ticker",
                "codes":["KRW-BTC"],
                "isOnlyRealtime": True
            },

            # Format Field
            {
                "format":"SIMPLE"
            }
        ]
        subscribe_data = json.dumps(subscribe_fmt)
        await websocket.send(subscribe_data)

        while True:
            data = await websocket.recv()
            await asyncio.sleep(1)
            data = json.loads(data)
            cur_price=data["tp"]
            print("Cur Price : " , cur_price, type(cur_price))
            ring_buffer.enque(cur_price)
            print("Buffer Size : ", ring_buffer.no)

            if ring_buffer.is_full():
                ring_buffer.dump()
                ring_buffer.plot_single_graph()
                break

async def main(ring_buffer:RingBuffer):
    await upbit_ws_client(ring_buffer)

if __name__=='__main__':
    # User Setting
    buffer_capacity=10

    ring_buf=RingBuffer(capacity=buffer_capacity)

    asyncio.run(main(ring_buf))