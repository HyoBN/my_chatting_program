
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

--------------

### GIL(Global Interpreter Lock)

 - 파이썬에서 쓰레드를 여러 개 생성한다고 해서 여러 개의 쓰레드가 동시에 실행되지 않는다. 정확히 특정 시점에는 단 하나의 쓰레드만 실행된다. 
 - 즉, 하나의 쓰레드에 모든 자원에 접근하는 것을 허락하고 그 후에는 Lock을 걸어 다른 쓰레드는 실행할 수 없게 막아버리는 것이다.
 - 파이썬의 메모리 관리 체계가 기본적으로 Thread-unsafe하기 때문에 Thread Safety한 환경을 만들기 위해 Mutex를 통해 한 시점에 단 하나의 쓰레드만 실행되도록 만든 것이다.
 
 - Context Switching 비용이 적게 들고 구현하기 효율적이지만 한 번에 한 쓰레드만이 코드를 실행시킬 수 있기 때문에 멀티 쓰레드 환경에서는 성능 저하를 불러오는 문제가 있다.
 - 하지만 내가 구현하는 프로그램 수준에서는 신경쓰지 않아도 될 정도이다.
 
--------------
 
### 현재 시각 출력하기.

```python
import datetime

now = datetime.datetime.now()
nowTime = now.strftime('%H:%m') # 07:35 가 출력됨.

```

 - strfime 메소드는 시간 튜플을 받아 로컬 시간의 문자열 표현을 반환하므로 출력 형태를 원하는대로 설정할 수 있다.
 - ex) now.strftime('시각 : [%H:%m]')  # 시각 : [10:30] 으로 출력됨.

--------------

### 파이썬 전역변수 특징.

파이썬의 객체들은 mutable / immutable 두 가지로 분류할 수 있다.  

#### immutable : 변경불가능한.
- call by value로 동작하여 값만 변경되더라도 새로운 객체로 생성 된다.
- 즉, 전역변수로 선언한 변수가 특정 함수 내에서 호출되어 사용되면 그 함수 내에서 지역변수로 새로 생성된다.
- 함수 내에서 전역변수의 값을 변경하기 위해서는 global 을 사용해야 한다.
- immutable 자료형 종류 : bool, int , str, tuple

#### mutable : 변경가능한.
- call by reference로 동작한다.
- 함수에 매개변수로 객체를 전달하면(parameter passing) global을 사용할 필요없이 객체의 일부를 indexing, slicing 등을 통해 변경할 수 있다.
- 하지만, 값을 재할당하려면 global을 사용해야 한다.
 
- mutable 자료형 종류 : list, dict, set

