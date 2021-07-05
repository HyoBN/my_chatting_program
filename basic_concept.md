
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

#### Time-wait 상태 빠져나오기.

>>  OSError: [Errno 98] Address already in use  
와 같은 에러가 뜬 경우, (주소할당 에러, Binding Error)

```python
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```
를 사용하면 해결할 수 있다.

--------------

#### 한글 인코딩,디코딩 관련.

> *UnicodeDecodeError:'utf-8' codec can't decode byte 0xbc in position 0:

과 같은 에러가 뜨는 이유는 한글 인코딩 방식 차이 때문인데  
인코딩 인자를 'utf-8'이 아닌 'cp949'로 변경해주면 된다.  

<인코딩 방식 차이에 관한 설명글>
https://studyforus.tistory.com/167