"""배경음악 합성(외부 음원 없음, numpy/scipy). 사용: python3 make-music.py out.wav [길이초=95] [변주=1] [종소리시작:간격]
변주 0~5는 조성·진행이 다릅니다(0 C장조, 1 가단조, 2 D장조, 3 마단조, 4 F장조, 5 G장조).
느린 피아노풍 아르페지오 + 패드 + 저음, 후반으로 갈수록 풍성해지고 마지막은 밝은 화음으로 맺습니다.
종소리시작:간격 을 주면 장면이 바뀌는 시점마다 가벼운 종소리를 얹습니다(예: 3.5:8)."""
import sys, numpy as np
from scipy.signal import fftconvolve
from scipy.io import wavfile
out=sys.argv[1] if len(sys.argv)>1 else 'music.wav'
DUR=float(sys.argv[2]) if len(sys.argv)>2 else 95.0
VAR=int(sys.argv[3]) if len(sys.argv)>3 else 1
ACC=sys.argv[4] if len(sys.argv)>4 else ''
SR=44100; N=int(SR*DUR); rng=np.random.default_rng(3+VAR)
hz=lambda m:440*2**((m-69)/12)
def pluck(m,dur,vel=1.0):
    n=int(SR*dur); t=np.arange(n)/SR; f=hz(m)
    s=np.sin(2*np.pi*f*t)+.35*np.sin(2*np.pi*2*f*t)*np.exp(-t*6)+.12*np.sin(2*np.pi*3*f*t)*np.exp(-t*9)
    return s*np.minimum(t/.008,1)*np.exp(-t*2.2)*vel
def pad(ms,dur):
    n=int(SR*dur); t=np.arange(n)/SR; o=np.zeros(n)
    for m in ms:
        for d in (-.12,0,.12): o+=np.sin(2*np.pi*hz(m)*2**(d/120)*t+rng.random()*6)
    return o*np.minimum(t/1.6,1)*np.minimum((dur-t)/1.6,1)/len(ms)/3
def tri(root,minor):
    th=3 if minor else 4
    return (root,[root,root+th,root+7],[root+12,root+12+th,root+19,root+24])
PROG={0:[(48,0),(45,1),(41,0),(43,0)],1:[(45,1),(41,0),(48,0),(43,0)],2:[(50,0),(47,1),(43,0),(45,0)],
      3:[(52,1),(48,0),(43,0),(50,0)],4:[(41,0),(38,1),(46,0),(48,0)],5:[(43,0),(40,1),(48,0),(50,0)]}
FIN={0:(72,76,79),1:(72,76,79),2:(74,78,81),3:(79,83,86),4:(77,81,84),5:(79,83,86)}
chords=[tri(r,m) for r,m in PROG[VAR%6]]
L=np.zeros(N); R=np.zeros(N)
def add(buf,sig,t0):
    i=int(t0*SR); j=min(N,i+len(sig))
    if 0<=i<N: buf[i:j]+=sig[:j-i]
CH=4.0; fin_len=min(8.0,DUR*.12); arp_start=2.0 if DUR<60 else 6.0; fast=VAR%2==0
for k in range(int(DUR/CH)+1):
    t0=k*CH; root,pd,arp=chords[k%4]
    if t0>=DUR-fin_len: root,pd,arp=chords[0]
    prog=min(1,t0/(.63*DUR))
    p=pad([x-12 for x in pd]+[pd[0]],CH+1.5)*(.55+.4*prog); add(L,p,t0); add(R,p,t0)
    b=pluck(root-12,CH,.9)*.6; add(L,b,t0); add(R,b,t0)
    if t0>=arp_start and t0<DUR-fin_len:
        busy=.46*DUR<=t0<.8*DUR; step=.5 if busy or fast and DUR<60 else 1.0
        pat=[0,1,2,3,2,1,2,3] if step==.5 else [0,2,1,3]
        for i,ix in enumerate(pat[:int(CH/step)]):
            s=pluck(arp[ix],2.6,.55+.25*prog)*(.8 if i%2 else 1); pan=.3+.4*((ix%4)/3)
            add(L,s*(1-pan),t0+i*step); add(R,s*pan*1.4,t0+i*step)
        if busy:
            s=pluck(arp[3]+12,3,.35); add(L,s*.5,t0+2); add(R,s*.8,t0+2)
fin=sum(pluck(m,min(6,fin_len),w) for m,w in zip(FIN[VAR%6],(.5,.4,.35)))
add(L,fin,DUR-fin_len+1); add(R,fin,DUR-fin_len+1)
if ACC:
    a0,st=[float(x) for x in ACC.split(':')]; tt=a0; i=0
    while tt<DUR-fin_len-1:
        top=chords[(int(tt/CH))%4][2][3]+(0,2,4,7)[i%4]; bell=pluck(top+12,2.2,.28)
        add(L,bell*.6,tt); add(R,bell*.9,tt); tt+=st; i+=1
imp=rng.standard_normal(int(SR*2.4))*np.exp(-np.arange(int(SR*2.4))/SR*2.2); imp/=np.abs(imp).sum()/6
rev=lambda x:x+.55*fftconvolve(x,imp)[:N]
L=rev(L); R=rev(R)
fade=np.minimum(np.arange(N)/(SR*2),1)*np.minimum((N-np.arange(N))/(SR*4),1)
st=np.stack([L*fade,R*fade],1); st/=np.abs(st).max()*1.15
wavfile.write(out,SR,(st*32767).astype(np.int16)); print('ok',out)
