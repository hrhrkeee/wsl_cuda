#!/bin/bash

# コピー元フォルダ
SOURCE_FOLDER="template/workspace"

# 対象となる workspace フォルダを検索し、ループで処理
for TARGET_FOLDER in **/workspace; do
    # ターゲットフォルダが存在するか確認
    if [ -d "$TARGET_FOLDER" ]; then
        echo "処理対象フォルダ: $TARGET_FOLDER"

        # workspace フォルダ内のすべてのファイルとディレクトリを削除
        echo "$TARGET_FOLDER 内のファイルを削除中..."
        rm -rf "${TARGET_FOLDER:?}/"*

        # template/workspace の内容を workspace にコピー
        echo "コピー中: $SOURCE_FOLDER から $TARGET_FOLDER へ"
        cp -r "$SOURCE_FOLDER/"* "$TARGET_FOLDER/"
    else
        echo "フォルダが見つかりません: $TARGET_FOLDER"
    fi
done

echo "処理完了"
