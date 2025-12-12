@echo off
REM ========================================
REM Preprocessing with VnCoreNLP
REM ========================================

echo.
echo ========================================
echo PREPROCESSING WITH VNCORENLP
echo ========================================
echo.

python scripts/preprocess_data.py ^
    --input-dir data/raw ^
    --output-dir data/processed_vncorenlp ^
    --vncorenlp-path "vncorenlp\VnCoreNLP-master\VnCoreNLP-1.1.1.jar"

echo.
echo ========================================
echo DONE!
echo ========================================
echo.
echo Output files:
echo   - data/processed_vncorenlp/train.csv
echo   - data/processed_vncorenlp/val.csv
echo   - data/processed_vncorenlp/test.csv
echo.
pause

