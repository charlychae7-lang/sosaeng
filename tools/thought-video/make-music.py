"""배경음악 합성 (95초, 스테레오). 외부 음원 없이 numpy로 직접 만듭니다.
Am – F – C – G 진행, 느린 피아노풍 아르페지오 + 패드 + 저음, 후반(④~⑤)으로 갈수록 풍성해지고 마지막은 C 화음으로 맺습니다.
사용: python3 make-music.py out.wav"""
import sys, numpy as np
from scipy.signal import fftconvolve
from scipy.io import wavfile
SR=44100; DUR=95.0; N=int(SR*DUR)
rng=np.random.default_rng(3)
def hz(m): return 440*2**((m-69)/12)
def pluck(m,dur,vel=1.0):
    n=int(SR*dur); t=np.arange(n)/SR; f=hz(m)
    s=np.sin(2*np.pi*f*t)+.35*np.sin(2*np.pi*2*f*t)*np.exp(-t*6)+.12*np.sin(2*np.pi*3*f*t)*np.exp(-t*9)
    env=np.minimum(t/.008,1)*np.exp(-t*2.2); return s*env*vel
def pad(ms,dur):
    n=int(SR*dur); t=np.arange(n)/SR; o=np.zeros(n)
    for m in ms:
        for d in (-.12,0,.12):
            f=hz(m)*2**(d/12/10); o+=np.sin(2*np.pi*f*t+rng.random()*6)
    a=np.minimum(t/1.6,1)*np.minimum((dur-t)/1.6,1); return o*a/len(ms)/3
L=np.zeros(N); R=np.zeros(N)
def add(buf,sig,t0,pan=0):
    i=int(t0*SR); j=min(N,i+len(sig))
    if i<N: buf[i:j]+=sig[:j-i]
chords=[(57,[57,60,64],[69,72,76,81]),(53,[53,57,60],[65,69,72,77]),(48,[55,60,64],[67,72,76,79]),(55,[55,59,62],[67,71,74,79])]
BEAT=2.0  # 한 화음 = 4박(8초)... 박당 1초 → 화음당 4초
CH=4.0; nch=int(DUR/CH)+1
for k in range(nch):
    t0=k*CH; root,pd,arp=chords[k%4]; last=t0+CH>=DUR-8
    if k>=22: root,pd,arp=48,[55,60,64],[67,72,76,79]
    prog=min(1,t0/60)   # 점점 풍성해짐
    p=pad([x-12 for x in pd]+[pd[0]],CH+1.5)*(.55+.4*prog)
    add(L,p,t0); add(R,p,t0)
    b=pluck(root-12,CH,.9)*.6; add(L,b,t0); add(R,b,t0)
    if t0>=6 and not (t0>=DUR-8):
        step=.5 if (t0>=44 and t0<76) else 1.0
        pat=[0,1,2,3,2,1,2,3] if step==.5 else [0,2,1,3]
        for i,ix in enumerate(pat[:int(CH/step)]):
            m=arp[ix]; s=pluck(m,2.6,.55+.25*prog)*(.8 if i%2 else 1)
            pan=.3+.4*((ix%4)/3)
            add(L,s*(1-pan),t0+i*step); add(R,s*pan*1.4+s*.0,t0+i*step)
    if t0>=44 and t0<76 and k%1==0:   # 생각이 물질이 되는 구간: 상행 멜로디
        mel=[arp[3]+(0 if k%2 else 2),arp[2]+12-12]
        s=pluck(arp[3]+12,3,.35); add(L,s*.5,t0+2); add(R,s*.8,t0+2)
# 마지막 맺음
fin=pluck(72,6,.5)+pluck(76,6,.4)+pluck(79,6,.35); add(L,fin,DUR-7); add(R,fin,DUR-7)
# 리버브
imp=rng.standard_normal(int(SR*2.4))*np.exp(-np.arange(int(SR*2.4))/SR*2.2); imp/=np.abs(imp).sum()/6
def rev(x): return x+.55*fftconvolve(x,imp)[:N]
L=rev(L); R=rev(R)
fade=np.minimum(np.arange(N)/(SR*2),1)*np.minimum((N-np.arange(N))/(SR*4),1)
st=np.stack([L*fade,R*fade],1); st/=np.abs(st).max()*1.15
wavfile.write(sys.argv[1] if len(sys.argv)>1 else 'music.wav',SR,(st*32767).astype(np.int16))
print('ok')
