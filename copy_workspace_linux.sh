#!/bin/bash

# コピー元フォルダを指定
SOURCE_FOLDER="template/workspace"

# 対象となる workspace フォルダを検索し、コピー元フォルダを除外して処理
for TARGET_FOLDER in **/workspace; do
    if [ "$TARGET_FOLDER" != "$SOURCE_FOLDER" ]; then
        echo "処理対象フォルダ: $TARGET_FOLDER"

        # workspace フォルダ内のすべてのファイルとディレクトリを削除
        echo "$TARGET_FOLDER 内のファイルを削除中..."
        rm -rf "${TARGET_FOLDER:?}/"*

        # コピー元フォルダの内容をコピー
        echo "コピー中: $SOURCE_FOLDER から $TARGET_FOLDER へ"
        cp -r "$SOURCE_FOLDER/"* "$TARGET_FOLDER/"
    fi
done

echo "処理完了"
