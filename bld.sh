export ARCH=arm64
export SUBARCH=ARM64
export KBUILD_BUILD_USER="aliza"
export KBUILD_BUILD_HOST="sad"
rm -rf out
export LD_LIBRARY_PATH="~/clang/lib64:$LD_LIBRARY_PATH}"
make O=out vendor/alioth_defconfig PATH="/workspaces/clang/bin:$PATH"
make O=out CC=clang -j$(nproc --all) PATH="/workspaces/clang/bin:$PATH" CROSS_COMPILE=aarch64-linux-gnu- LLVM=1 LLVM_IAS=1