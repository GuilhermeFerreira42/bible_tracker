@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

FOR %%f IN (*_BIBLIA_VIVA.pdf) DO (
    SET "nome_original=%%f"
    SET "nome_novo=!nome_original:_BIBLIA_VIVA=_BIBLIA_CATOLICA!"
    REN "!nome_original!" "!nome_novo!"
    IF EXIST "!nome_novo!" (
        ECHO Renomeado: !nome_original! para !nome_novo!
    ) ELSE (
        ECHO ERRO ao renomear: !nome_original!
    )
)
ENDLOCAL