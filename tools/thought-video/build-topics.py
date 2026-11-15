"""topics.src.html + index.html의 머리 윤곽(HEAD) 블록 → topics.html (렌더러가 읽는 파일)"""
src=open('index.html',encoding='utf8').read()
i=src.index("// 머리 윤곽"); j=src.index("// S1 분자 군집",i)
head=src[i:j]
t=open('topics.src.html',encoding='utf8').read().replace('/*HEAD*/',head)
open('topics.html','w',encoding='utf8').write(t); print('topics.html built')
