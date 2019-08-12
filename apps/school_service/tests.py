from django.test import TestCase

# Create your tests here.
import json

week = [12,13]
print(sum([pow(2,i) for i in week]))
print(','.join([str(i) for i in week]))
a = '[]'
print(json.loads(a))