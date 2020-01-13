'''
from journal.nature_group.nature import Nature
import article.article as article_module
import os

n1 = Nature()

n1.get_articles()

print(n1.articles)

'''
a = 1
b = 2

l = []
l += [a,b]

print(l)

l[0]=3

print(a)
print(l)