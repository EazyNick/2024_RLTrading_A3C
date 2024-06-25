# api/models.py
from django.db import models

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField()

    def __str__(self):
        return self.name

# 이 줄은 __str__ 메서드의 반환값을 정의합니다.
# MyModel 객체를 문자열로 변환할 때 name 속성의 값을 반환합니다.
# 예를 들어, MyModel 객체를 출력하면 name 속성에 설정된 값이 출력됩니다.