---    
title: "Home"    
date: 2019-08-13T06:48:42+09:00    
---    
    
# まだ改修中。 
- localhostではうまく行かないので、127.0.0.1:1313を使う必要がある。    
- https://gist.github.com/jeremybise/a6afea2d4c7f9044180ffeb663a617cf これそのうち役立ちそう  
- hogeフォルダの中に、いろいろ画像とかのリソースを入れておくとよさそう。  
- 記事の管理のため、`Date-Name`な感じにする。  
- listがうまく機能してない→empty cache and reloadで治った

## checklist
- `hugo new posts/hoge/index.md`でいける  
- 後ろスペース二個以上で改行っぽいのでreplaceを最後にかける  
- `cp -r public/* docs/`  
- CNAMEを忘れずに