#!/bin/sh

set -e

ICON=ic_launcher.icns
if [ "$RUNNER_OS" = "Windows" ]; then
    ICON=ic_launcher.ico
fi

# Icon is used on Mac and ignored on Linux
pyinstaller \
    --hidden-import ciphwren_dav.radicale \
    --hidden-import radicale.auth.htpasswd \
    --hidden-import radicale.hook.none \
    --additional-hooks-dir ./hooks \
    --onefile \
    --windowed \
    --icon $ICON \
    ../scripts/ciphwren-dav

# Travis stuff
mkdir -p deploy
ARCH=$(uname -m)
if [ "$RUNNER_OS" = "Linux" ]; then
    ./dist/ciphwren-dav --version  # Sanity test on Linux and mac, can't do on windows
    if [ "$ARCH" = "x86_64" ]; then
        mv dist/ciphwren-dav "deploy/linux-amd64-ciphwren-dav"
    elif [ "$ARCH" = "aarch64" ]; then
        mv dist/ciphwren-dav "deploy/linux-arm64-ciphwren-dav"
    else
        echo "Unsupported architecture: $ARCH"
        exit 1
    fi

fi
if [ "$RUNNER_OS" = "macOS" ]; then
    ./dist/ciphwren-dav --version  # Sanity test on Linux and mac, can't do on windows
    cd dist
    zip -r "mac-$ARCH-ciphwren-dav.zip" *
    mv "mac-$ARCH-ciphwren-dav.zip" ../deploy/
    cd ../
fi
if [ "$RUNNER_OS" = "Windows" ]; then
    mv dist/ciphwren-dav.exe deploy/
fi
