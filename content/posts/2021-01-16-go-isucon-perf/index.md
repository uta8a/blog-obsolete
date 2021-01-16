---
date: "2021-01-16T17:07:46+09:00"
title: "読書: やってみようGoでISUCONパフォーマンスチューニングーISUCON7の予想問題を試してみる本ー"
type: "post"
draft: false
---

- 読んだ本: https://booth.pm/ja/items/1035782
- 以前りゅーそうさんという方の [はじめてのUIデザインの教科書をフロントエンジニアの方と読んだ](https://ryusou.dev/posts/beginner-uidesignbook) という記事を読み、誰かこれやりませんかと積読リストを公開したところ、 [あいのざさん](https://twitter.com/ainoz10) からリプライ頂いたので読んで感想を通話で話しました。
- アイデアの元になったりゅーそうさん、もやし丸さん、そして乗ってきてくださたあいのざさん、ありがとうございます。

## # 積読解消会の進め方
- 読む本を決めて、DMで進捗を報告しながら読み進める(今回は30ページほどの本だったが、環境構築など、手を動かす必要があった)
- 報告はこんな感じ: 今日は15ページまで進めました。環境構築で詰まったところはgistに置きました(gistのリンク)
- だいたいお互い終了したところで通話する日程を決める
- こんな感じ: discordで土曜日の14:00-15:00にやる(実際は14:30-16:30になった)
- (りゅーそうさんのブログには2時間とあったが、初めて話す相手なので1時間とっておいて、後ろは予定を入れず延長可能にしておいた)
- お話する
- 終わり

## # まとめと感想
- goならalpとpprof
- 本体のソースコードの他に、nginxなどミドルウェアにも詳しくなる必要がある。
- 最初にISUCONに挑戦しても分からないと思うので、この本のようなチュートリアルはありがたい。得点も10倍になって簡単な修正で一気に点数が上がってとても楽しい
- 普段ゼロからWebアプリを書くと自分で書いたので勝手が分かるが、ISUCONのように他の人の書いたものだと勝手が分からない。経験値が必要。
- ISUCONの典型が知りたい。パフォーマンスチューニングのまずこれを疑え！的な典型集が欲しい。

## # 本書を現在(2021/01/16)やると遭遇するトラブルシューティング

## ## xbuild go-installが動かない
- Conohaでは気にしなくてよいです。
- vagrantでやる場合、 https://github.com/matsuu/vagrant-isucon を使うとxbuildが失敗する。
- goの公式ページに従ってバイナリをwget/curlしてインストールする

## ## pprofを実行するときにtauが必要
- pprofを入れると、tauがないと言われる
- 以下のように対応し、go toolから実行する

```shell
sudo apt-get install tau
go tool pprof localhost:8080 ~/isubata/webapp/go/src/isubata http://localhost:6060/debug/pprof/profile?seconds=60
```

## ## go-sql-driverが使えない
- go v1.9で `go get go-sql-driver` すると、Builder周りのv1.10の機能をつかっているためにgoのビルドが通らない
- 以下のように、ライブラリ部分でgit checkoutして過去のタグがつけられたcommitに戻ると使えるようになる。

```shell
go get github.com/go-sql-driver/mysql
cd github.com/
mkdir go-sql-driver
cd go-sql-driver
git clone https://github.com/go-sql-driver/mysql.git
git checkout v1.4
```

## # 今後やってみたいこと
- ISUCON7qualでさらなる改良をする。特に、今回は書籍に書いてあることしかしていないので、自力で考え出して(アイデアパート)自力で実装したい(実装パート)
- ISUCONの典型をまとめたい。ISUCON慣れしたい。
- ましさんのN+1検出ツール https://mesimasi.com/mercari_go_one/ のようなツールを試してみたい。これを使うためにはgoのバージョンを上げる必要があるので、ついでにUbuntu20.04対応をしたい。(ansible書き換え)
- mini ISUCON 練習会を身内でやってみたい。ISUCONの運営楽しそうすぎる。(競技環境のホスティングのように、高度に厳しい状況でインフラをするの楽しそう)
