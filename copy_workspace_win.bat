@echo off
setlocal

:: template/workspace からコピーする元フォルダを指定
set SOURCE_FOLDER=template\workspace

:: 対象となるワイルドカードパスの workspace フォルダを検索して処理
for /d %%D in (**\workspace) do (
    echo 処理対象フォルダ: %%D

    :: コピー先フォルダの内容をすべて削除
    echo %%D 内のファイルを削除中...
    rd /s /q "%%D"
    mkdir "%%D"

    :: ファイルをコピー
    echo コピー中: %SOURCE_FOLDER% から %%D へ
    xcopy /e /i /h /y "%SOURCE_FOLDER%\*" "%%D\"
)

echo 処理完了
pause
endlocal
