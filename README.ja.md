# Apply Modifiers With Shape Keys

> 他の言語で読む: [English](README.md), [日本語](README.ja.md)

## 概要

シェイプキーのあるメッシュにモディファイアを適用するアドオンの Blender 2.8 対応バージョンです。

元のバージョンは [mato.sus304](https://sites.google.com/site/matosus304blendernotes/home) さんによるオープンソースソフトウェア(GPLv2)です。

## 使い方

### インストール

- [Releaseページ](../../releases)から最新版のzipをダウンロードしてください

- Blenderの設定ウィンドウにあるアドオンパネルからInstallボタンを押して、さっきダウンロードしたzipファイルを選びます

- アドオン一覧に'Apply Modifiers With Shape Keys'が追加されるので、有効にします

- メニューの *Object > Apply* の中に 'Apply All Modifiers With Shape Keys' 'Apply Selected Modifiers With Shape Keys' 'Apply Pose As Rest Pose With Shape Keys' の３つが追加されます

モディファイアを適用したいオブジェクトを選択状態にした上で上記のメニューを実行すると、シェイプキーをなるべく維持したままモディファイアを適用できます。

シェイプキーのないオブジェクトに対しては標準の適用と同じ動作をします。

### Apply all modifiers with shape keys

選択されたすべてのオブジェクトに対して、すべての有効なモディファイアを一度に適用します。

### Apply selected modifier with shape keys

アクティブなオブジェクト一つに対して、適用するモディファイアを選択して、シェイプキーを維持しつつ適用します。

### Apply pose as rest pose with shape keys

選択されたすべてのアーマチュアオブジェクトに対し、現在のビューレイヤーに存在するメッシュオブジェクトの中から選択されているアーマチュアを参照しているものに対してシェイプキーを維持しつつアーマチュアモディファイアを適用した後アーマチュアモディファイアを復元し、現在のポースをレストポーズとして適用します。

## 制限

このアドオンはシェイプキーの数だけオブジェクトを複製して、それぞれにモディファイアを適用後それらをシェイプキーとして登録し直すという動作をします。

そのためミラーモデファイアなど頂点数が増減するモディファイアでは、シェイプキーによっては対応する頂点を特定できないため正常に処理できない場合があります。

## ライセンス

[GNU GENERAL PUBLIC LICENSE (v2)](LICENSE)
