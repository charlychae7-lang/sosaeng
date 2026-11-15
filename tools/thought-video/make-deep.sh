#!/bin/bash
# 깊이 읽기 주제별 세로형 영상 일괄 제작: ./make-deep.sh 1 2 3 ... (번호 생략 시 1~19)
# 결과: ../../app/media/deep/NN-slug.mp4 (1080×1920, 배경음악 포함)
cd "$(dirname "$0")"; export NODE_PATH=$(npm root -g); python3 build-topics.py >/dev/null
OUT=../../app/media/deep; TMP=${TMPDIR:-/tmp}/deep; mkdir -p $OUT $TMP
for n in ${@:-$(seq 1 19)}; do
  slug=$(node -e "global.TOPICS=null;const s=require('fs').readFileSync('topics-data.js','utf8');const T=eval(s+';TOPICS');const t=T.find(x=>x.n==$n);console.log(String(t.n).padStart(2,'0')+'-'+t.slug+' '+t.v)")
  name=${slug% *}; var=${slug#* }
  CRF=${CRF:-23} node render.js video $TMP/$name-silent.mp4 --topic $n >/dev/null || exit 1
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $TMP/$name-silent.mp4)
  python3 make-music.py $TMP/$name.wav $dur $var 3.5:8 >/dev/null
  ffmpeg -y -loglevel error -i $TMP/$name-silent.mp4 -i $TMP/$name.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k -shortest -movflags +faststart $OUT/$name.mp4
  echo "done $name"
done
