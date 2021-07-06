
### 파이썬 멀티스레딩(Multi Threading)

```python
from threading import *

x = Thread(target=yhb, args=('A',))

x.start()

```

 - target : 쓰레드가 실행할 함수를 지정.
 - args : target으로 지정한 함수에 넘길 인자.
 - start() 함수를 실행하면 해당 쓰레드가 시작된다.
    - 주의할 점) args의 자료형이 튜플이기 때문에 인자가 하나일 경우 뒤에 콤마(,)를 반드시 붙여 줘야한다.
    - 튜플 자료형 개념) https://wikidocs.net/15
    
----------

### Time-wait 상태 빠져나오기.

>>  OSError: [Errno 98] Address already in use  
와 같은 에러가 뜬 경우, (주소할당 에러, Binding Error)

```python
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```
를 사용하면 해결할 수 있다.

--------------

### 한글 인코딩,디코딩 관련.

> *UnicodeDecodeError:'utf-8' codec can't decode byte 0xbc in position 0:

과 같은 에러가 뜨는 이유는 한글 인코딩 방식 차이 때문인데  
인코딩 인자를 'utf-8'이 아닌 'cp949'로 변경해주면 된다.  

<인코딩 방식 차이에 관한 설명글>
https://studyforus.tistory.com/167

----------------

### 멀멀멀

#### 멀티 프로세스
 : 말그래도 프로세스를 여러 개 이용하는 것.
- 하나의 프로세스에 하나의 클라이언트를 책임진다.
- Context switching으로 인한 시스템 저하 발생.

※ Context switching : CPU가 하나의 Task(Process / Thread)를 실행하고 있는 상태에서 Interrupt 요청에 의해 다른 Task로 전환될 때 기존의 Task 상태 및 Register 값들에 대한 정보(Context)를 저장하고 새로운 Task의 Context 정보로 교체하는 작업. 

- 프로세스를 늘리는 것은 상대적으로 비효율적이다.

#### 멀티 쓰레드
 쓰레드 : 프로세스 안에서 논리적으로 동작하는 하나의 작업단위.
- 같은 프로세스에 공존하는 쓰레드는 서로 힙, 코드, 데이터 영역을 공유하므로 서로 통신할 때 전역변수나 힙 영역을 사용한다.
- 전역변수를 사용할 때는 데이터의 일관성을 위해 mutex를 활용해 동기화 시켜준다.  
    - ※ mutex : 동 시간에 하나의 쓰레드만이 임계 영역에 접근할 수 있도록 막아 데이터의 일관성을 유지한다.
- 멀티쓰레드 또한 Context Switching으로 인한 성능 저하가 발생한다. 쓰레드의 수가 늘어날수록 임계영역(Critical Section)에 접근하기 위한 대기 시간이 늘어난다.
- 이러한 문제를 해결하기 위해 블로킹 개념 등장, 멀티 플렉싱이 생겨났다.

#### 멀티 플렉싱

- 멀티 쓰레드에서 read, write 시의 문제점을 해결하기 위해 등장.
- 클라이언트에게 데이터가 오지 않을 경우 블로킹 상태를 유지하여 효율성을 높인다.
- 하나의 쓰레드가 여러개의 클라이언트를 관리할 수 있다.
- 코드 구현이 조금 복잡하다.