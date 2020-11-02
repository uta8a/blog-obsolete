---
date: "2020-11-03T07:29:55+09:00"
title: "F#でちょっと遊ぶ - 1 - 単純な電卓"
type: "post"
draft: true
---

- F#って言語機能が強くて、Haskellのような、言語処理系界のスーパーカーに見えます。(個人の感想です。)
- 今回は「F#の言語機能を使うためにコードを書く」という本末転倒の目標を掲げて、初心者がF#をおそるおそる触ってみる記事です。間違いや、「こうすればもっと面白いよ！」といった指摘やアドバイスがもしあれば、 [Twitter: @kaito_tateyama](https://twitter.com/kaito_tateyama) へリプライかDMで連絡いただけると嬉しいです。

# F#の導入
- 必要なものは以下の通りです。
```text
dotnet # .NET Core CLI
fantomas # formatter
```
- インストール方法です。まずdotnetを入れていきます。Ubuntuだと https://docs.microsoft.com/en-us/dotnet/core/install/linux-debian を見ておくとよさそうです。
- 今回は言語機能が知りたいだけなので、現時点での最新であるdotnet 5.0(preview)を入れます。(私が使っているOSはUbuntu20.04です)
```shell
$ dotnet-sdk.dotnet --version
5.0.100-rc.2.20479.15
# https://github.com/dotnet/core/blob/master/release-notes/5.0/preview/5.0.0-rc.2-install-instructions.md
```
- 次にformatterを入れます
```shell
$ dotnet-sdk.dotnet tool install -g fantomas-tool
$ fantomas Program.fs # format
```
- F#ではプロジェクトという単位を作り、その中にファイルをいくつかおいて実行します。(ファイル単体でスクリプトのようにも扱えるらしい？)
- new, runといったコマンドを覚えるのが面倒なのでMakefileを作っています。
```makefile
arg = "default"
target = "Program.fs"
new:
	@dotnet-sdk.dotnet new console -lang="F#" -o ./${arg}
	@cp .gitignore ./${arg}/.gitignore
run:
	@dotnet-sdk.dotnet run --project ./${arg}
fmt:
	@fantomas ./${target}
```
- 以下のようにしていきます
```shell
$ make arg=Name new # make project
$ make arg=Name run # run project
$ make target=Name/Program.fs fmt # format project
```
- 以下を実行すると、ハローワールドできると思います
```shell
make arg=minilang new
make arg=minilang run
# Hello world from F#
```

# ディレクトリ構成
- ディレクトリ構成を見ていきます。
```text
minilang/
├── bin/
├── minilang.fsproj
├── obj/
├── Program.fs
├── .gitignore
└── README.md
```
- bin/とobj/はgitignoreします。
- Program.fsがスタート地点になります。(ファイルの中を見ると、`[<EntryPoint>]`があります。ここが開始地点です)
<!-- ファイル分割のときの話 -->

# ファイルの中身を出力する
- ここでの目標は「Eitherを使う」ということです。
<!-- ファイル読み込みと、エラーを出して確認 -->

# test?そろそろテスト駆動にしたい