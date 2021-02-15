# leetcode-testing-service

## Usage 
```python3 ./oo_app.py```

OR with Docker 

```docker build -t etoor/python-testing-service:1.0.1```
```docker run -t 1000:5000 .```

## See /python/app.py and def test() for the main function that is currently being worked on 

Endpoints: 
1. http://127.0.0.1:5000/api/test?q=add_nums&data=def%20add_nums(a%2Cb)%3A%0A%20%20return%20a%20%2B%20b%20%2B%201%20
2. http://127.0.0.1:5000/api/test?q=add_nums&data=def%20add_nums(a%2Cb)%3A%0A%20%20return%20a%20%2B%20b


OO Endpoints: 
1. http://localhost:5000/api/run?q=anotha_one&data=class%20Solution%3A%0A%09def%20anotha_one(self%2C%20a%2C%20b)%3A%0A%09%09return%20a%20%2B%20b&testcase=1%0A2
2. http://localhost:5000/api/submit?q=anotha_one&data=class%20Solution%3A%0A%09def%20anotha_one(self%2C%20a%2C%20b)%3A%0A%09%09return%20a%20%2B%20b