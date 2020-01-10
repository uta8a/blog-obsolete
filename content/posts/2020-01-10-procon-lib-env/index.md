---  
date: "2020-01-10T08:13:00+09:00"  
title: "競プロ用ライブラリuta8alibの環境構築"  
type: "post"  
draft: false  
---  
  
[uta8alib](https://github.com/uta8a/uta8alib)という競技プログラミング用ライブラリの環境構築について書きます。  
今回環境を作るに当たって、[ngtkanaさん](https://github.com/ngtkana)の[ngtlib](https://github.com/ngtkana/ngtlib)を参考にした部分が大きいです。ありがとうございました。  
  
# やりたいこと  
- C++とRustで競プロをする  
- `example/main.rs`のように、ファイル名を`main.[rs|cpp|hpp]`で統一したい  
- testを行い、CIでcheckする  
- ライブラリのコピペを行いたいので、コードとテストは別ファイルにしたい(特にRust)  
- あとでdocument(html)を生成することを考えて、コメントを各ファイルとテストに書けるようにしておく  
- git submoduleを使ってみる(C++テストフレームワークCatch2の使用)  
  
**今後の展望**  
  
- status badgeをGitHubにつける  
- [How to run CI on your library for competitive programming](https://online-judge-tools.readthedocs.io/en/master/run-ci-on-your-library.ja.html)を参考に、今後Verifyを導入してCIを回す  
- Git-Flowを参考に、featureブランチでライブラリ単体を開発してC++とRustが揃ったらdevelopブランチに統合、masterにまとめてマージするときにCIを走らせる  
- snippetの導入。コードからコメントを抜いたものをsnippetファイルとして自動生成したい。(VSCode, neovim(dein.vim, UltiSnip))  
- ライブラリの種類を増やす(たくさん問題を解きましょう)  
  
# 開発の流れ  
  
- [ディレクトリ構成を決める](#ディレクトリ構成を決める)  
- [自分用の競プロCLIツール、chanを使う](#自分用の競プロcliツール-chanを使う)  
- [git submoduleを使う](#git-submoduleを使う)  
- [Rustのテスト方法を考える](#rustのテスト方法を考える)  
- [C++のテスト方法を考える](#c-のテスト方法を考える)  
- [Gitの開発手順を見直す](#gitの開発手順を見直す)  
- [CIでテストを回す](#ciでテストを回す)  
  
## ディレクトリ構成を決める  
  
ディレクトリ構成は以下のようになっています。  
srcの下にcppとrustがあり、その下にディレクトリが存在していて`example`などがライブラリの名前になります。コードはそのディレクトリの中の`main.[rs|hpp]`に書きます。  
testはテストコードです。srcと同様の構成になっています。  
```  
❯ tree -I 'Catch2|chan|cpp-test|rust-test'  
.  
├── CMakeLists.txt  
├── Dockerfile  
├── libtest.sh  
├── README.md  
├── src  
│   ├── cpp  
│   │   ├── example  
│   │   │   └── main.hpp  
│   │   └── include  
│   │       └── lib.hpp  
│   └── rust  
│       └── example  
│           └── main.rs  
├── test  
│   ├── cpp  
│   │   ├── CMakeLists.txt  
│   │   ├── example  
│   │   │   └── main.cpp  
│   │   └── main.cpp  
│   └── rust  
│       └── example  
│           └── main.rs  
└── todo.md  
```  
重視したことは、少しくらい深さのある構成になっても自分が好きな方を選ぶということです。`lib-name.hpp`というような名前のファイルをフラットに`src`直下に置く方も多いですが、僕は`lib-name/main.hpp`の方が好きなのでこうしました。好みの問題ですね。  
深さができてGitHubで見るには面倒、という弱点のために、documentを自動生成してブラウザで見る、というようにしたいです。コードブロックの右上にコピペボタンを用意すれば捗りそうです。  
  
## 自分用の競プロCLIツール、chanを使う  
  
競プロをするときは焦りがちなので、使うコマンドは最小限にしたいです。あと、打ちやすいほうがいい。僕は`chan`というコマンドでコンパイルして実行ファイル生成を行っていましたが、このコマンドにライブラリのテンプレート作成機能をもたせることにしました。  
```  
chan main.rs # rustc main.rsが走る  
chan main.cpp # g++ が走る  
/path/to/uta8alib$ chan generate cpp example # exampleという名前のフォルダで、C++のsrcとtestのテンプレートファイル作成。C++の場合、include/lib.hppにパスを追加する。  
```  
引数の数で判別しています。単純な機能ですが、Rustで4時間くらいかけて書いて、Python3とかの方がこういうのは向いてるなぁと感じました。外部crateは使いませんでしたが、[`clap-rs`](https://github.com/clap-rs/clap)を使うと高機能にできそうです。ソースコードの本体は[こちら](https://github.com/uta8a/chan/blob/171f0719af55ed7542cee27fb2ae4b11e98483d8/src/main.rs)です。  
重視したことは、色付きで出力させることです。はじめOptionなしでは色がなく、読みづらく感じていました。調べたところ、強制的にcoloringをONにするOptionをつければよいと分かりました。Rustは `rustc --color=always` を、C++は `g++ -fdiagnostics-color=always` を指定しています。  
  
## git submoduleを使う  
  
[ngtlib](https://github.com/ngtkana/ngtlib)を見てgit submoduleに興味が湧いていました。また、競プロに関わることは普段はなるべくひとつにまとめておきたいものです。というわけでchanをsubmoduleとしてuta8alibに取り込みます。  
  
**やること**  
  
- [`chan`](https://github.com/uta8a/chan/tree/master)をGitHubに上げます。   
- `uta8alib$ git submodule add git@github.com:uta8a/chan.git chan`でsubmoduleを追加  
- ここで、`add repo directory`のrepoとdirectoryに気をつけましょう。  
- .gitmodulesが自動生成されるので確認  
```  
[submodule "chan"]  
	path = chan  
	url = git@github.com:uta8a/chan.git  
```  
- こんな感じならOK  
- あとはchanに入って`cargo build --release`でバイナリを作り、aliasで`chan`を使えるようにしておく。  
  
**読むべき**  
  
- [git公式](https://git-scm.com/docs/git-submodule) submoduleの後に`--help`を入れて打っておよい。  
  
**困った時のコマンド**  
  
- git cloneしてきたらsubmoduleがない！  
  - `git submodule update --init --recursive`  
- submoduleが更新された。新しくしたい。  
  - `git submodule foreach git pull origin master`  
  
**注意**  
  
- `.gitmodules`を書いて`git submodule pull`みたいなことをやりたいが、それはできない。`add`で追加して、`.gitmodules`は生成物と捉えたほうがよい。  
  
## Rustのテスト方法を考える  
  
今回、cargoで外部crateを入れるつもりはなかったので、cargoを使わないディレクトリ構成をしていました。しかしテストをするにはcargoがよいです。そこで、テストのときに`cargo new`して`cargo test`するという方法に決めました。  
[`libtest.sh`](https://github.com/uta8a/uta8alib/blob/master/libtest.sh)の `# rust test` の箇所を見ると分かるのですが、catでsrcとtestのファイルを結合したものを`cargo new`で生成したディレクトリの中に入れて、`lib.rs`に追記しています。  
`cargo`を完全にテストツールとして使っていて強引な気がしますがうまく行っています。一つのファイルにまとめているのでprivate method testができ、わざわざ `pub` をつけずにライブラリを書くことが出来ます。  
  
## C++のテスト方法を考える  
  
[git submoduleを使う](#git-submoduleを使う)と同じ手順で[Catch2](https://github.com/catchorg/Catch2)を導入しました。  
  
**やること**  
  
- google testやcatch2など、C++テストフレームワークを検討する  
- catch2の使い方を調べる  
- cmakeを理解する  
- testを書く  
- CMakeLists.txtを書く  
- makeを通す  
  
細かく分けるとこんな感じでした。テストフレームワークの選定については[wikipediaのユニットテストフレームワークの記事のC++の欄](https://ja.wikipedia.org/wiki/%E3%83%A6%E3%83%8B%E3%83%83%E3%83%88%E3%83%86%E3%82%B9%E3%83%88%E3%83%BB%E3%83%95%E3%83%AC%E3%83%BC%E3%83%A0%E3%83%AF%E3%83%BC%E3%82%AF%E4%B8%80%E8%A6%A7#C++)を参考にしました。  
  
> ヘッダ・ファイルのみからなり、外部に依存しない。(wikipediaの記事より引用)  
  
たくさんあるのでgoogle testとCatch2しか見れませんでしたが、違いがいまいち分からなかったので[ngtlib](https://github.com/ngtkana/ngtlib)でも使われているCatch2を選択しました。  
CMakeLists.tstについては[ngtlib](https://github.com/ngtkana/ngtlib)を参考にしたいのであまり理解できていません。以下の記事が参考になりました。  
  
**参考**  
  
- [CMakeの使い方](https://qiita.com/shohirose/items/45fb49c6b429e8b204ac)  
  - 簡単なところから説明されているので分かりやすいです  
- [cmakeでgoogletestできる環境を作ってみる](https://www.jonki.net/entry/2016/06/15/220029)  
  - `ctest --verbose`を使うとデバッグが捗ります  
- [シェルスクリプトで相対パスと絶対パスを取得する](https://www.task-notes.com/entry/20150214/1423882800)  
  - `pwd`とシェルスクリプトに書く時の注意点です  
  
makeが通った時は嬉しかったです。  
  
## Gitの開発手順を見直す  
  
ここまでずっとmasterにpushしてきましたが、そろそろCIを導入するとなると、masterにプルリク送ったときのみCIが回るようにしたいです。現在はdevelopとmasterの2つですが、ライブラリを作る時は`feature-xxx`というブランチを作り、RustとC++が揃った段階でdevelopに取り込み、masterへマージしてCI回すという形にしたいです。  
  
**参考**  
  
- [Git-flowって何？](https://qiita.com/KosukeSone/items/514dd24828b485c69a05)  
  
## CIでテストを回す  
  
以前GitHub Actionsを使ったことがあったので、今回はCircle CIを使ってみました。結論の`config.yml`は[こちら](https://github.com/uta8a/uta8alib/blob/master/.circleci/config.yml)です。  
```  
version: 2.0  
  
jobs:  
  build_and_test:  
    docker:  
      - image: uta8a/circleci-rust-cmake:0.0.1  
    environment:  
      USER: uta8a  
    working_directory: ~/work  
    steps:  
      - checkout  
      - run: git submodule sync  
      - run: git submodule update --init  
      - run: ./libtest.sh  
  
workflows:  
  version: 2  
  build:  
    jobs:  
      - build_and_test:  
          filters:  
            branches:  
              only: master  
```  
  
**注意**  
  
- 現在version 2.1まで指定できますが、localのcircleci CLIツールが2.0までしか対応していないので2.0を指定します。  
- dockerで2つimageを指定しようとしたら最初の一つしか反映されませんでした。無料枠であることが関係していそうですが原因は分かりませんでした。  
  - そのため、DockerHubに自分で作ったイメージを上げました。[DockerHubへのリンク](https://hub.docker.com/r/uta8a/circleci-rust-cmake)  
  - これは、`circleci/rust`をベースにして[`rikorose/gcc-make`](https://hub.docker.com/r/rikorose/gcc-cmake/)を参考に書き足しています。gccは8で、cmakeは3.15でした。  
- `cargo`をdockerで使おうとすると`$USER`が足りないというエラーが出ます。そのため、environmentでUSERを指定します。  
- git submoduleを使っている場合は、checkout後にsubmoduleも引っ張ってくるようコマンドを指定します。  
- branchはmasterのみに設定します  
- workflowsのversionは、全体のversionが2.1のときは記述がいらないのですが、2.0では必須です。  
- circleciのデバッグ作業はローカルのCLIツールを用いましょう。`circleci config validate`でyamlが正しいかどうか判定でき、`circleci local execute --job build_and_test`で特定のjobを実際に回せます(dockerを使います)  
  
## status badgeをGitHubにつける  
  
[公式のdocument](https://circleci.com/docs/2.0/status-badges/)を読むと簡単に導入できます。Different Styleの方が好みだったのでそうしました。  
  
# 今後の展望  
  
## Logoを作ってやる気を高める  
## Verifyしてみる  
## snippetの導入  
## 競プロで使うエディタの選定  
## どこでも競プロできるようにシェルスクリプトを書く  
## ライブラリの種類をどうやって増やすか(アルゴリズムを学ぶ)  
  
# この記事を書くに当たって  
  
`[article](#toc)` で見出しへのanchor linkが張れるのですが、これは一癖あって、hugoで生成されたもののidをみながらそれと一致するようにやっていくとよいです。例えば、 `##C++でのテスト方法を考える` は `#c--でのテスト方法を考える` に変化します。  
  
# 終わりに  
  
今回環境構築がメインでもう力尽きそうですがここからがスタートラインです。今年は競プロのレートに興味を持たずに、アルゴリズムに興味を持つことを目標にしていきたいです。  
