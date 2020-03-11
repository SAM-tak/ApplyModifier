# Apply Modifiers With Shape Keys

> 他の言語で読む: [English](README.md), [日本語](README.ja.md)

## 概要

シェイプキーのあるメッシュにモディファイアを適用するアドオンの Blender 2.8 対応バージョンです。

元のバージョンは [mato.sus304](https://sites.google.com/site/matosus304blendernotes/home) さんによるオープンソースソフトウェア(GPLv2)です。

## 使い方

- Release タブから最新版のzipをダウンロードしてください

- Blenderの設定ウィンドウにあるアドオンパネルからInstallボタンを押して、さっきダウンロードしたzipファイルを選びます

- アドオン一覧に'Apply Modifiers With Shape Keys'が追加されるので、有効にします

- メニューの *Object > Apply* の中に 'Apply all modifiers' 'Apply selected modifiers' の２つが追加されます

モディファイアを適用したいオブジェクトを選択状態にした上で上記のメニューを実行すると、シェイプキーをなるべく維持したままモディファイアを適用できます。

シェイプキーのないオブジェクトに対しては標準の適用と同じ動作をしますので、わざわざこの機能を使う必要はないです。

### Apply all modifires with shape keys

すべての有効なモディファイアを一度に適用します。

### Apply selected modifire with shape keys

適用するモディファイアを選択して、シェイプキーを維持しつつ適用します。

## 制限

このアドオンはシェイプキーの数だけオブジェクトを複製して、それぞれにモディファイアを適用後それらをシェイプキーとして登録し直すという動作をします。

そのためミラーモデファイアなど頂点数が増減するモディファイアでは、シェイプキーによっては対応する頂点を特定できないため正常に処理できない場合があります。

## ライセンス

[GNU GENERAL PUBLIC LICENSE (v2)](LICENSE)
