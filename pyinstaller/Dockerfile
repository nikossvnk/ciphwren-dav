# Builds a standalone executable from the ciphwren-dav docker image.
#
# Build the ciphwren-dav image first (docker build -t ciphwren-dav .), and then
# docker build -t ciphwren-dav-bundle -f pyinstaller/Dockerfile .
# docker run --rm -it -u $(id -u):$(id -g) -v $(pwd):/repo ciphwren-dav-bundle

FROM ciphwren-dav

USER root

RUN pip install PyInstaller

USER ciphwren

ENTRYPOINT ["bash"]
CMD ["-c", "cd /repo/pyinstaller && ./bundle.sh"]
