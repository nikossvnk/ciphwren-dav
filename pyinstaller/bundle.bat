pyinstaller ^
    --hidden-import ciphwren_dav.radicale ^
    --hidden-import radicale.auth.htpasswd ^
    --hidden-import radicale.hook.none ^
    --hidden-import radicale.group.none ^
    --hidden-import radicale.sharing.none ^
    --additional-hooks-dir .\hooks ^
    --onefile ^
    --windowed ^
    --icon .\ic_launcher.ico ^
    ..\scripts\ciphwren-dav
